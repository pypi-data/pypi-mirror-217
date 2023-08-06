from operator import itemgetter
from intervaltree import Interval
from collections.abc import Iterable
from scipy.stats import chi2_contingency
from scipy.signal import find_peaks
from Bio.Seq import reverse_complement, translate
from Bio.Data.CodonTable import TranslationError
from pysam import FastaFile
import numpy as np
import copy
import itertools
from cpmodule import fickett, FrameKmer  # this is from the CPAT module
from .splice_graph import SegmentGraph
from .short_read import Coverage
from ._transcriptome_filter import SPLICE_CATEGORY
from ._utils import pairwise, _filter_event, find_longest_orf, smooth, get_quantiles, _filter_function, \
    pairwise_event_test, prepare_contingency_table, cmp_dist

import logging
logger = logging.getLogger('isotools')


class Gene(Interval):
    'This class stores all gene information and transcripts. It is derived from intervaltree.Interval.'
    required_infos = ['ID', 'chr', 'strand']

    # initialization
    def __new__(cls, begin, end, data, transcriptome):
        return super().__new__(cls, begin, end, data)  # required as Interval (and Gene) is immutable

    def __init__(self, begin, end, data, transcriptome):
        self._transcriptome = transcriptome

    def __str__(self):
        return 'Gene {} {}({}), {} reference transcripts, {} expressed transcripts'.format(
            self.name, self.region, self.strand, self.n_ref_transcripts, self.n_transcripts)

    def __repr__(self):
        return object.__repr__(self)

    from ._gene_plots import sashimi_plot, gene_track, sashimi_plot_short_reads, sashimi_figure, plot_domains
    from .domains import add_interpro_domains

    def short_reads(self, idx):
        '''Returns the short read coverage profile for a short read sample.

        :param idx: The index of the short read sample.
        :returns: The short read coverage profile.'''

        try:
            return self.data['short_reads'][idx]
        except (KeyError, IndexError):
            srdf = self._transcriptome.infos['short_reads']  # raises key_error if no short reads added
            self.data.setdefault('short_reads', [])
            for i in range(len(self.data['short_reads']), len(srdf)):
                self.data['short_reads'].append(Coverage.from_bam(srdf.file[i], self))
        return self.data['short_reads'][idx]

    def correct_fuzzy_junctions(self, trid, size, modify=True):
        '''Corrects for splicing shifts.

         This function looks for "shifted junctions", e.g. same difference compared to reference annotation at both donor and acceptor)
         presumably caused by ambiguous alignments. In these cases the positions are adapted to the reference position (if modify is set).

         :param trid: The index of the transcript to be checked.
         :param size: The maximum shift to be corrected.
         :param modify: If set, the exon positions are corrected according to the reference.
         :returns: A dictionary with the exon id as keys and the shifted bases as values.'''

        exons = trid['exons']
        shifts = self.ref_segment_graph.fuzzy_junction(exons, size)
        if shifts and modify:
            for i, sh in shifts.items():
                if exons[i][0] <= exons[i][1] + sh and exons[i + 1][0] + sh <= exons[i + 1][1]:
                    exons[i][1] += sh
                    exons[i + 1][0] += sh
            trid['exons'] = [e for e in exons if e[0] < e[1]]  # remove zero length exons
        return shifts

    def _to_gtf(self, trids, ref_trids=None, source='isoseq', ref_source='annotation'):
        '''Creates the gtf lines of the gene as strings.'''
        donotshow = {'transcripts', 'short_exons', 'segment_graph'}
        info = {'gene_id': self.id, 'gene_name': self.name}
        lines = [None]
        starts = []
        ends = []
        ref_fsm = []
        for i in trids:
            tr = self.transcripts[i]
            info['transcript_id'] = f'{info["gene_id"]}_{i}'
            starts.append(tr['exons'][0][0] + 1)
            ends.append(tr['exons'][-1][1])
            trinfo = info.copy()
            if 'downstream_A_content' in tr:
                trinfo['downstream_A_content'] = f'{tr["downstream_A_content"]:0.3f}'
            if tr['annotation'][0] == 0:  # FSM
                refinfo = {}
                for refid in tr['annotation'][1]['FSM']:
                    ref_fsm.append(refid)
                    for k in self.ref_transcripts[refid]:
                        if k == 'exons':
                            continue
                        elif k == 'CDS':
                            if self.strand == '+':
                                cds_start, cds_end = self.ref_transcripts[refid]['CDS']
                            else:
                                cds_end, cds_start = self.ref_transcripts[refid]['CDS']
                            refinfo.setdefault('CDS_start', []).append(str(cds_start))
                            refinfo.setdefault('CDS_end', []).append(str(cds_end))
                        else:
                            refinfo.setdefault(k, []).append(str(self.ref_transcripts[refid][k]))
                for k, vlist in refinfo.items():
                    trinfo[f'ref_{k}'] = ','.join(vlist)
            else:
                trinfo['novelty'] = ','.join(k for k in tr['annotation'][1])
            lines.append((self.chrom, source, 'transcript', tr['exons'][0][0] + 1, tr['exons'][-1][1], '.',
                         self.strand, '.', '; '.join(f'{k} "{v}"' for k, v in trinfo.items())))
            noncanonical = tr.get('noncanonical_splicing', [])
            for enr, pos in enumerate(tr['exons']):
                exon_info = info.copy()
                exon_info['exon_id'] = f'{info["gene_id"]}_{i}_{enr}'
                if enr in noncanonical:
                    exon_info['noncanonical_donor'] = noncanonical[enr][:2]
                if enr+1 in noncanonical:
                    exon_info['noncanonical_acceptor'] = noncanonical[enr+1][2:]
                lines.append((self.chrom, source, 'exon', pos[0] + 1, pos[1], '.', self.strand, '.', '; '.join(f'{k} "{v}"' for k, v in exon_info.items())))
        if ref_trids:
            # add reference transcripts not covered by FSM
            for i, tr in enumerate(self.ref_transcripts):
                if i in ref_fsm:
                    continue
                starts.append(tr['exons'][0][0] + 1)
                ends.append(tr['exons'][-1][1])
                info['transcript_id'] = f'{info["gene_id"]}_ref{i}'
                refinfo = info.copy()
                for k in tr:
                    if k == 'exons':
                        continue
                    elif k == 'CDS':
                        if self.strand == '+':
                            cds_start, cds_end = tr['CDS']
                        else:
                            cds_end, cds_start = tr['CDS']
                        refinfo['CDS_start'] = str(cds_start)
                        refinfo['CDS_end'] = str(cds_end)
                    else:
                        refinfo.setdefault(k, []).append(str(tr[k]))
                    lines.append((self.chrom, ref_source, 'transcript', tr['exons'][0][0] + 1, tr['exons'][-1][1], '.',
                                  self.strand, '.', '; '.join(f'{k} "{v}"' for k, v in refinfo.items())))
                    for enr, pos in enumerate(tr['exons']):
                        exon_info = info.copy()
                        exon_id = f'{info["gene_id"]}_ref{i}_{enr}'
                        lines.append((self.chrom, ref_source, 'exon', pos[0] + 1, pos[1], '.', self.strand, '.', f'exon_id "{exon_id}"'))

        if len(lines) > 1:
            # add gene line
            if 'reference' in self.data:
                info.update({k: v for k, v in self.data['reference'].items() if k not in donotshow})  # add reference gene specific fields
            lines[0] = (self.chrom, source, 'gene', min(starts), max(ends), '.', self.strand, '.', '; '.join(f'{k} "{v}"' for k, v in info.items()))
            return lines
        return []

    def add_noncanonical_splicing(self, genome_fh):
        '''Add information on noncanonical splicing.

        For all transcripts of the gene, scan for noncanonical (i.e. not GT-AG) splice sites.
        If noncanonical splice sites are present, the corresponding intron index (in genomic orientation) and the sequence
        i.e. the di-nucleotides of donor and acceptor as XX-YY string are stored in the "noncannoncical_splicing" field of the transcript dicts.
        True noncanonical splicing is rare, thus it might indicate technical artifacts (template switching, misalignment, ...)

        :param genome_fh: A file handle of the genome fastA file.'''
        ss_seq = {}
        for tr in self.transcripts:
            pos = [(tr['exons'][i][1], tr['exons'][i + 1][0] - 2) for i in range(len(tr['exons']) - 1)]
            new_ss_seq = {site: genome_fh.fetch(self.chrom, site, site + 2).upper() for intron in pos for site in intron if site not in ss_seq}
            if new_ss_seq:
                ss_seq.update(new_ss_seq)

            if self.strand == '+':
                sj_seq = [ss_seq[d] + ss_seq[a] for d, a in pos]
            else:
                sj_seq = [reverse_complement(ss_seq[d] + ss_seq[a]) for d, a in pos]

            nc = [(i, seq) for i, seq in enumerate(sj_seq) if seq != 'GTAG']
            if nc:
                tr['noncanonical_splicing'] = nc

    def add_direct_repeat_len(self, genome_fh, delta=15, max_mm=2, wobble=2):
        '''Computes direct repeat length.

        This function counts the number of consecutive equal bases at donor and acceptor sites of the splice junctions.
        This information is stored in the "direct_repeat_len" filed of the transcript dictionaries.
        Direct repeats longer than expected by chance indicate template switching.

        :param genome_fh: The file handle to the genome fastA.
        :param delta: The maximum length of direct repeats that can be found.
        :param max_mm: The maximum length of direct repeats that can be found.
        :param wobble: The maximum length of direct repeats that can be found.'''

        intron_seq = {}
        score = {}

        for tr in self.transcripts:
            for intron in ((tr['exons'][i][1], tr['exons'][i + 1][0]) for i in range(len(tr['exons']) - 1)):
                for pos in intron:
                    try:
                        intron_seq.setdefault(pos, genome_fh.fetch(self.chrom, pos - delta, pos + delta))
                    except (ValueError, IndexError):  # N padding at start/end of the chromosomes
                        chr_len = genome_fh.get_reference_length(self.chrom)
                        seq = genome_fh.fetch(self.chrom, max(0, pos - delta), min(chr_len, pos + delta))
                        if pos - delta < 0:
                            seq = ''.join(['N'] * (pos - delta)) + seq
                        if pos + delta > chr_len:
                            seq += ''.join(['N'] * (pos + delta - chr_len))
                        intron_seq.setdefault(pos, seq)
                if intron not in score:
                    score[intron] = repeat_len(intron_seq[intron[0]], intron_seq[intron[1]], wobble=wobble, max_mm=max_mm)

        for tr in self.transcripts:
            tr['direct_repeat_len'] = [min(score[(e1[1], e2[0])], delta) for e1, e2 in pairwise(tr['exons'])]

    def add_threeprime_a_content(self, genome_fh, length=30):
        '''Adds the information of the genomic A content downstream the transcript.

        High values of genomic A content indicate internal priming and hence genomic origin of the LRTS read.
        This function populates the 'downstream_A_content' field of the transcript dictionaries.

        :param geneome_fh: A file handle for the indexed genome fastA file.
        :param length: The length of the downstream region to be considered.
        '''
        a_content = {}
        for tr in (t for tL in (self.transcripts, self.ref_transcripts) for t in tL):
            if self.strand == '+':
                pos = tr['exons'][-1][1]
            else:
                pos = tr['exons'][0][0] - length
            if pos not in a_content:
                seq = genome_fh.fetch(self.chrom, max(0, pos), pos + length)
                if self.strand == '+':
                    a_content[pos] = seq.upper().count('A') / length
                else:
                    a_content[pos] = seq.upper().count('T') / length
            tr['downstream_A_content'] = a_content[pos]

    def get_sequence(self, genome_fh, trids=None, reference=False, protein=False):
        '''Returns the nucleotide sequence of the specified transcripts.

        :param genome_fh: The path to the genome fastA file, or FastaFile handle.
        :param trids: List of transcript ids for which the sequence are requested.
        :param reference: Specify whether the sequence is fetched for reference transcripts (True)
            or long read transcripts (False, default).
        :param protein: Return protein sequences instead of transcript sequences.
        :returns: A dictionary of transcript ids and their sequences.
        '''

        trL = [(i, tr) for i, tr in enumerate(self.ref_transcripts if reference else self.transcripts) if trids is None or i in trids]
        if not trL:
            return {}
        pos = (min(tr['exons'][0][0] for _, tr in trL), max(tr['exons'][-1][1] for _, tr in trL))
        try:  # assume its a FastaFile file handle
            seq = genome_fh.fetch(self.chrom, *pos)
        except AttributeError:
            genome_fn = genome_fh
            with FastaFile(genome_fn) as genome_fh:
                seq = genome_fh.fetch(self.chrom, *pos)
        tr_seqs = {}
        for i, tr in trL:
            trseq = ''
            for e in tr['exons']:
                trseq += seq[e[0]-pos[0]:e[1]-pos[0]]
            tr_seqs[i] = trseq

        if self.strand == '-':
            tr_seqs = {i: reverse_complement(ts) for i, ts in tr_seqs.items()}
        if not protein:
            return tr_seqs
        prot_seqs = {}
        for i, tr in trL:
            orf = tr.get("CDS", tr.get("ORF"))
            if not orf:
                continue
            pos = sorted(self.find_transcript_positions(i, orf[:2], reference=reference))
            try:
                prot_seqs[i] = translate(tr_seqs[i][pos[0]:pos[1]], cds=True)
            except TranslationError:
                logger.warning(f'CDS sequence of {self.id} {"reference" if reference else ""} transcript {i} cannot be translated.')
        return prot_seqs

    def add_orfs(self, genome_fh, reference=False, minlen=30, start_codons=["ATG"], stop_codons=['TAA', 'TAG', 'TGA'],
                 get_fickett=True, coding_hexamers=None, noncoding_hexamers=None):
        '''Find longest ORF for each transcript.

        For each transcript, the longest ORF (sequence starting with start_condon, and ending with in frame stop codon) is determined.
        The genomic and transcript positions of these codons, and the length of the ORF, as well as  the number of upstream start codons
        is added to the transcript properties tr["ORF"]. Additionally, the Fickett score, and the hexamer score are computed. For the
        latter, hexamer frequencies in coding and noncoding transcripts are needed. See CPAT python module for prebuilt tables and
        instructions.
        :param minlen: the minimum length of a ORF (in bases) to be considered.
        :param start_codons: List of base triplets that are considered as start codons. By default ['ATG'].
        :param stop_codons: List of base triplets that are considered as stop codons. By default ['TAA', 'TAG', 'TGA'].
        :param coding_hexamers: The hexamer frequencies for coding sequences.
        :param noncoding_hexamers: The hexamer frequencies for coding sequences.'''

        trL = self.ref_transcripts if reference else self.transcripts
        for trid, tr_seq in self.get_sequence(genome_fh, reference=reference).items():
            try:
                start, stop, frame, seq_start, seq_end, uORFs = find_longest_orf(
                    tr_seq, start_codons, stop_codons, coding_hexamers, noncoding_hexamers)
            except TypeError:  # No ORF
                continue
            if stop is None or stop - start < minlen:
                continue

            tr = trL[trid]
            tr_start = tr['exons'][0][0]
            cum_exon_len = np.cumsum([end-start for start, end in tr['exons']])  # cumulative exon length
            cum_intron_len = np.cumsum([0]+[end-start for (_, start), (end, _) in pairwise(tr['exons'])])  # cumulative intron length
            if self.strand == '-':
                fwd_start, fwd_stop = cum_exon_len[-1]-stop, cum_exon_len[-1]-start
            else:
                fwd_start, fwd_stop = start, stop  # start/stop position wrt genomic fwd strand
            start_exon = next(i for i in range(len(cum_exon_len)) if cum_exon_len[i] >= fwd_start)
            stop_exon = next(i for i in range(start_exon, len(cum_exon_len)) if cum_exon_len[i] >= fwd_stop)
            genome_pos = (tr_start+fwd_start+cum_intron_len[start_exon],
                          tr_start+fwd_stop+cum_intron_len[stop_exon])
            dist_pas = 0  # distance of termination codon to last upstream splice site
            if self.strand == '+' and stop_exon < len(cum_exon_len)-1:
                dist_pas = cum_exon_len[-2]-fwd_stop
            if self.strand == '-' and start_exon > 0:
                dist_pas = fwd_start-cum_exon_len[0]
            orf_dict = {"5'UTR": start, 'CDS': stop-start, "3'UTR": cum_exon_len[-1]-stop,
                        'start_codon': seq_start, 'stop_codon': seq_end, 'NMD': dist_pas > 55, 'uORFs': uORFs}

            if coding_hexamers is not None and noncoding_hexamers is not None:
                orf_dict['hexamer'] = FrameKmer.kmer_ratio(tr_seq[start:stop], 6, 3, coding_hexamers, noncoding_hexamers)
            if get_fickett:
                orf_dict['fickett'] = fickett.fickett_value(tr_seq[start:stop])
            tr['ORF'] = (*genome_pos, orf_dict)

    def add_fragments(self):
        '''Checks for transcripts that are fully contained in other transcripts.

        Transcripts that are fully contained in other transcripts are potential truncations.
        This function populates the 'fragment' filed of the transcript dictionaries with the indices of the containing transcripts,
        and the exon ids that match the first and last exons.'''

        for trid, containers in self.segment_graph.find_fragments().items():
            self.transcripts[trid]['fragments'] = containers  # list of (containing transcript id, first 5' exons, first 3'exons)

    def coding_len(self, trid):
        '''Returns length of 5\'UTR, coding sequence and 3\'UTR.

        :param trid: The transcript index for which the coding length is requested. '''

        try:
            exons = self.transcripts[trid]['exons']
            cds = self.transcripts[trid]['CDS']
        except KeyError:
            return None
        else:
            coding_len = _coding_len(exons, cds)
        if self.strand == '-':
            coding_len.reverse()
        return coding_len

    def get_infos(self, trid, keys, sample_i, group_i, **kwargs):
        '''Returns the transcript information specified in "keys" as a list.'''
        return [value for k in keys for value in self._get_info(trid, k, sample_i, group_i)]

    def _get_info(self, trid, key, sample_i, group_i, **kwargs):
        # returns tuples (as some keys return multiple values)
        if key == 'length':
            return sum((e - b for b, e in self.transcripts[trid]['exons'])),
        elif key == 'n_exons':
            return len(self.transcripts[trid]['exons']),
        elif key == 'exon_starts':
            return ','.join(str(e[0]) for e in self.transcripts[trid]['exons']),
        elif key == 'exon_ends':
            return ','.join(str(e[1]) for e in self.transcripts[trid]['exons']),
        elif key == 'annotation':
            # sel=['sj_i','base_i', 'as']
            if 'annotation' not in self.transcripts[trid]:
                return ('NA',) * 2
            nov_class, subcat = self.transcripts[trid]['annotation']
            # subcat_string = ';'.join(k if v is None else '{}:{}'.format(k, v) for k, v in subcat.items())
            return SPLICE_CATEGORY[nov_class], ','.join(subcat)  # only the names of the subcategories
        elif key == 'coverage':
            return self.coverage[sample_i, trid]
        elif key == 'tpm':
            return self.tpm(kwargs.get('pseudocount', 1))[sample_i, trid]
        elif key == 'group_coverage_sum':
            return tuple(self.coverage[si, trid].sum() for si in group_i)
        elif key == 'group_tpm_mean':
            return tuple(self.tpm(kwargs.get('pseudocount', 1))[si, trid].mean() for si in group_i)
        elif key in self.transcripts[trid]:
            val = self.transcripts[trid][key]
            if isinstance(val, Iterable):  # iterables get converted to string
                return str(val),
            else:
                return val,  # atomic (e.g. numeric)
        return 'NA',

    def _set_coverage(self, force=False):
        samples = self._transcriptome.samples
        cov = np.zeros((len(samples), self.n_transcripts), dtype=int)
        if not force:  # keep the segment graph if no new transcripts
            known = self.data.get('coverage', None)
            if known is not None and known.shape[1] == self.n_transcripts:
                if known.shape == cov.shape:
                    return
                cov[:known.shape[0], :] = known
                for i in range(known.shape[0], len(samples)):
                    for j, tr in enumerate(self.transcripts):
                        cov[i, j] = tr['coverage'].get(samples[i], 0)
                self.data['coverage'] = cov
                return
        for i, sa in enumerate(samples):
            for j, tr in enumerate(self.transcripts):
                cov[i, j] = tr['coverage'].get(sa, 0)
        self.data['coverage'] = cov
        self.data['segment_graph'] = None

    def tpm(self, pseudocount=1):
        '''Returns the transcripts per million (TPM).

        TPM is returned as a numpy array, with samples in columns and transcript isoforms in the rows.'''
        return (self.coverage+pseudocount)/self._transcriptome.sample_table['nonchimeric_reads'].values.reshape(-1, 1)*1e6

    def find_transcript_positions(self, trid, pos, reference=False):
        '''Converts genomic positions to positions within the transcript.

        :param trid: The transcript id
        :param pos: List of sorted genomic positions, for which the transcript positions are computed.'''

        tr_pos = []
        exons = self.ref_transcripts[trid]['exons'] if reference else self.transcripts[trid]['exons']
        e_idx = 0
        offset = 0
        for p in sorted(pos):
            try:
                while p > exons[e_idx][1]:
                    offset += (exons[e_idx][1]-exons[e_idx][0])
                    e_idx += 1

            except IndexError:
                for _ in range(len(pos)-len(tr_pos)):
                    tr_pos.append(None)
                break
            tr_pos.append(offset+p-exons[e_idx][0] if p >= exons[e_idx][0] else None)
        if self.strand == '-':
            trlen = sum(end-start for start, end in exons)
            tr_pos = [None if p is None else trlen-p for p in tr_pos]
        return tr_pos

    @property
    def coverage(self):
        '''Returns the transcript coverage.

        Coverage is returned as a numpy array, with samples in columns and transcript isoforms in the rows.'''
        cov = self.data.get('coverage', None)
        if cov is not None:
            return cov
        self._set_coverage()
        return self.data['coverage']

    @property
    def gene_coverage(self):
        '''Returns the gene coverage.

        Total Coverage of the gene for each sample.'''

        return self.coverage.sum(1)

    @property
    def chrom(self):
        '''Returns the genes chromosome.'''
        return self.data['chr']

    @property
    def start(self):  # alias for begin
        return self.begin

    @property
    def region(self):
        '''Returns the region of the gene as a string in the format "chr:start-end".'''
        try:
            return '{}:{}-{}'.format(self.chrom, self.start, self.end)
        except KeyError:
            raise

    @property
    def id(self):
        '''Returns the gene id'''
        try:
            return self.data['ID']
        except KeyError:
            logger.error(self.data)
            raise

    @property
    def name(self):
        '''Returns the gene name'''
        try:
            return self.data['name']
        except KeyError:
            return self.id  # e.g. novel genes do not have a name (but id)

    @property
    def is_annotated(self):
        '''Returns "True" iff reference annotation is present for the gene.'''
        return 'reference' in self.data

    @property
    def is_expressed(self):
        '''Returns "True" iff gene is covered by at least one long read in at least one sample.'''
        return bool(self.transcripts)

    @property
    def strand(self):
        '''Returns the strand of the gene, e.g. "+" or "-"'''
        return self.data['strand']

    @property
    def transcripts(self):
        '''Returns the list of transcripts of the gene, as found by LRTS.'''
        try:
            return self.data['transcripts']
        except KeyError:
            return []

    @property
    def ref_transcripts(self):
        '''Returns the list of reference transcripts of the gene.'''
        try:
            return self.data['reference']['transcripts']
        except KeyError:
            return []

    @property
    def n_transcripts(self):
        '''Returns number of transcripts of the gene, as found by LRTS.'''
        return len(self.transcripts)

    @property
    def n_ref_transcripts(self):
        '''Returns number of reference transcripts of the gene.'''
        return len(self.ref_transcripts)

    @property
    def ref_segment_graph(self):  # raises key error if not self.is_annotated
        '''Returns the segment graph of the reference transcripts for the gene'''

        assert self.is_annotated, "reference segment graph requested on novel gene"
        if 'segment_graph' not in self.data['reference'] or self.data['reference']['segment_graph'] is None:
            exons = [tr['exons'] for tr in self.ref_transcripts]
            self.data['reference']['segment_graph'] = SegmentGraph(exons, self.strand)
        return self.data['reference']['segment_graph']

    @property
    def segment_graph(self):
        '''Returns the segment graph of the LRTS transcripts for the gene'''
        if 'segment_graph' not in self.data or self.data['segment_graph'] is None:
            exons = [tr['exons'] for tr in self.transcripts]
            try:
                self.data['segment_graph'] = SegmentGraph(exons, self.strand)
            except Exception:
                logger.error('Error initializing Segment Graph on %s with exons %s', self.strand, exons)
                raise
        return self.data['segment_graph']

    def __copy__(self):
        return Gene(self.start, self.end, self.data, self._transcriptome)

    def __deepcopy__(self, memo):  # does not copy _transcriptome!
        return Gene(self.start, self.end, copy.deepcopy(self.data, memo), self._transcriptome)

    def __reduce__(self):
        return Gene, (self.start, self.end, self.data, self._transcriptome)

    def copy(self):
        'Returns a shallow copy of self.'
        return self.__copy__()

    def filter_transcripts(self, query=None, min_coverage=None, max_coverage=None):
        if query:
            tr_filter = self._transcriptome.filter['transcript']
            # used_tags={tag for tag in re.findall(r'\b\w+\b', query) if tag not in BOOL_OP}
            query_fun, used_tags = _filter_function(query)
            msg = 'did not find the following filter rules: {}\nvalid rules are: {}'
            assert all(f in tr_filter for f in used_tags), msg.format(
                ', '.join(f for f in used_tags if f not in tr_filter), ', '.join(tr_filter))
            tr_filter_fun = {tag: _filter_function(tr_filter[tag])[0] for tag in used_tags if tag in tr_filter}
        trids = []
        for i, tr in enumerate(self.transcripts):
            if min_coverage and self.coverage[:, i].sum() < min_coverage:
                continue
            if max_coverage and self.coverage[:, i].sum() > max_coverage:
                continue
            if query is None or query_fun(
                    **{tag: f(g=self, trid=i, **tr) for tag, f in tr_filter_fun.items()}):
                trids.append(i)
        return trids

    def filter_ref_transcripts(self, query=None):
        if query:
            tr_filter = self._transcriptome.filter['reference']
            # used_tags={tag for tag in re.findall(r'\b\w+\b', query) if tag not in BOOL_OP}
            query_fun, used_tags = _filter_function(query)
            msg = 'did not find the following filter rules: {}\nvalid rules are: {}'
            assert all(f in tr_filter for f in used_tags), msg.format(
                ', '.join(f for f in used_tags if f not in tr_filter), ', '.join(tr_filter))
            tr_filter_fun = {tag: _filter_function(tr_filter[tag])[0] for tag in used_tags if tag in tr_filter}
        else:
            return list(range(len(self.ref_transcripts)))
        trids = []
        for i, tr in enumerate(self.ref_transcripts):
            if query_fun(**{tag: f(g=self, trid=i, **tr) for tag, f in tr_filter_fun.items()}):
                trids.append(i)
        return trids

    def _find_splice_sites(exons, transcripts):
        '''Checks whether the splice sites of a new transcript are present in the set of transcripts.
        avoids the computation of segment graph, which provides the same functionality.

        :param exons: A list of exon tuples representing the transcript
        :type exons: list
        :return: boolean array indicating whether the splice site is contained or not'''

        intron_iter = [pairwise(tr['exons']) for tr in transcripts]
        current = [next(tr) for tr in intron_iter]
        contained = np.zeros(len(exons)-1)
        for j, (e1, e2) in enumerate(pairwise(exons)):
            for i, tr in enumerate(intron_iter):
                while current[i][0][1] < e1[1]:
                    try:
                        current[i] = next(tr)
                    except StopIteration:
                        continue
                if e1[1] == current[i][0][1] and e2[0] == current[i][1][0]:
                    contained[j] = True
        return current

    def coordination_test(self, samples=None, test="chi2", min_dist=1, min_total=100, min_alt_fraction=.1,
                          events=None, event_type=("ES", "5AS", "3AS", "IR", "ME")):
        '''Performs pairwise independence test for all pairs of Alternative Splicing Events (ASEs) in a gene.

        For all pairs of ASEs in a gene creates a contingency table and performs an indeppendence test.
        All ASEs A have two states, pri_A and alt_A, the primary and the alternative state respectivley.
        Thus, given two events A and B, we have four possible ways in which these events can occur on
        a transcript, that is, pri_A and pri_B, pri_A and alt_B, alt_A and pri_B, and alt_A and alt_B.
        These four values can be put in a contingency table and independence, or coordination,
        between the two events can be tested.

        :param samples: Specify the samples that should be considdered in the test.
            The samples can be provided either as a single group name, a list of sample names, or a list of sample indices.
        :param test: Test to be performed. One of ("chi2", "fisher")
        :type test: str
        :param min_dist: Minimum distance (in nucleotides) between the two
            alternative splicing events for the pair to be tested.
        :type min_dist: int
        :param min_total: The minimum total number of reads for an event pair to pass the filter.
        :type min_total: int
        :param min_alt_fraction: The minimum fraction of reads supporting the minor alternative of the two events.
        :type min_alt_fraction: float
        :param events: To speed up testing on different groups of the same transcriptome objects, events can be precomputed
            with the isotools._utils.precompute_events_dict function.
        :param event_type:  A tuple with event types to test. Valid types are
            ("ES", "3AS", "5AS", "IR", "ME", "TSS", "PAS"). Default is ("ES", "5AS", "3AS", "IR", "ME").
            Not used if the event parameter is already given.
        :return: A list of tuples with the test results: (gene_id, gene_name, strand, eventA_type, eventB_type,
            eventA_start, eventA_end, eventB_start, eventB_end, p_value, test_stat, log2OR,  dcPSI_AB, dcPSI_BA,
            priA_priB, priA_altB, altA_priB, altA_altB,  priA_priB_trids, priA_altB_trids, altA_priB_trids, altA_altB_trids).
        '''

        if samples is None:
            cov = self.coverage.sum(axis=0)
        else:
            try:
                # Fast mode when testing several genes
                cov = self.coverage[samples].sum(0)
            except IndexError:
                # Fall back to looking up the sample indices
                from isotools._transcriptome_stats import _check_groups
                _, _, groups = _check_groups(self._transcriptome, [samples], 1)
                cov = self.coverage[groups[0]].sum(0)

        sg = self.segment_graph

        if events is None:
            events = sg.find_splice_bubbles(types=event_type)

        events = [e for e in events if _filter_event(cov, e, min_total=min_total,
                                                     min_alt_fraction=min_alt_fraction)]
        # make sure its sorted (according to gene strand)
        if self.strand == '+':
            events.sort(key=itemgetter(2, 3), reverse=False)  # sort by starting node
        else:
            events.sort(key=itemgetter(3, 2), reverse=True)  # reverse sort by end node
        test_res = []

        for i, j in itertools.combinations(range(len(events)), 2):
            if sg.events_dist(events[i], events[j]) < min_dist:
                continue
            if (events[i][4], events[j][4]) == ("TSS", "TSS") or (events[i][4], events[j][4]) == ("PAS", "PAS"):
                continue

            con_tab, tr_ID_tab = prepare_contingency_table(events[i], events[j], cov)

            if con_tab.sum(None) < min_total:  # check that the joint occurrence of the two events passes the threshold
                continue
            if min(con_tab.sum(1).min(), con_tab.sum(0).min())/con_tab.sum(None) < min_alt_fraction:
                continue
            test_result = pairwise_event_test(con_tab, test=test)  # append to test result

            coordinate1 = sg._get_event_coordinate(events[i])
            coordinate2 = sg._get_event_coordinate(events[j])

            attr = (self.id, self.name, self.strand, events[i][4], events[j][4]) + \
                coordinate1 + coordinate2 + test_result + \
                tuple(con_tab.flatten()) + tuple(tr_ID_tab.flatten())

            # events[i][4] is the events[i] type
            # coordinate1[0] is the starting coordinate of event 1
            # coordinate1[0] is the ending coordinate of event 1
            # coordinate2[0] is the starting coordinate of event 2
            # coordinate2[1] is the ending coordinate of event 2

            test_res.append(attr)

        return test_res

    def die_test(self, groups, min_cov=25, n_isoforms=10):
        ''' Reimplementation of the DIE test, suggested by Joglekar et al in Nat Commun 12, 463 (2021):
        "A spatially resolved brain region- and cell type-specific isoform atlas of the postnatal mouse brain"

        Syntax and parameters follow the original implementation in
        https://github.com/noush-joglekar/scisorseqr/blob/master/inst/RScript/IsoformTest.R
        :param groups: Define the columns for the groups.
        :param min_cov: Minimal number of reads per group for the gene.
        :param n_isoforms: Number of isoforms to consider in the test for the gene. All additional least expressed isoforms get summarized.'''
        # select the samples and sum the group counts
        try:
            # Fast mode when testing several genes
            cov = np.array([self.coverage[grp].sum(0) for grp in groups]).T
        except IndexError:
            # Fall back to looking up the sample indices
            from isotools._transcriptome_stats import _check_groups
            _, _, groups = _check_groups(self._transcriptome, groups)
            cov = np.array([self.coverage[grp].sum(0) for grp in groups]).T

        if np.any(cov.sum(0) < min_cov):
            return np.nan, np.nan, []
        # if there are more than 'numIsoforms' isoforms of the gene, all additional least expressed get summarized.
        if cov.shape[0] > n_isoforms:
            idx = np.argpartition(-cov.sum(1), n_isoforms)  # take the n_isoforms most expressed isoforms (random order)
            additional = cov[idx[n_isoforms:]].sum(0)
            cov = cov[idx[:n_isoforms]]
            cov[n_isoforms-1] += additional
            idx[n_isoforms-1] = -1  # this isoform gets all other - I give it index
        elif cov.shape[0] < 2:
            return np.nan, np.nan, []
        else:
            idx = np.array(range(cov.shape[0]))
        try:
            _, pval, _, _ = chi2_contingency(cov)
        except ValueError:
            logger.error(f'chi2_contingency({cov})')
            raise
        iso_frac = cov/cov.sum(0)
        deltaPI = iso_frac[..., 0]-iso_frac[..., 1]
        order = np.argsort(deltaPI)
        pos_idx = [order[-i] for i in range(1, 3) if deltaPI[order[-i]] > 0]
        neg_idx = [order[i] for i in range(2) if deltaPI[order[i]] < 0]
        deltaPI_pos = deltaPI[pos_idx].sum()
        deltaPI_neg = deltaPI[neg_idx].sum()
        if deltaPI_pos > -deltaPI_neg:
            return pval, deltaPI_pos, idx[pos_idx]
        else:
            return pval, deltaPI_neg, idx[neg_idx]

    def _unify_ends(self, smooth_window=31, rel_prominence=1, search_range=(.1, .9)):
        ''' Find common TSS/PAS for tanscripts of the gene'''
        if not self.transcripts:
            # nothing to do here
            return
        assert 0 <= search_range[0] <= .5 <= search_range[1] <= 1
        # get gene tss/pas profiles
        tss = {}
        pas = {}
        strand = 1 if self.strand == '+' else -1
        for tr in self.transcripts:
            for sa in tr['TSS']:
                for pos, c in tr['TSS'][sa].items():
                    tss[pos] = tss.get(pos, 0)+c
            for sa in tr['PAS']:
                for pos, c in tr['PAS'][sa].items():
                    pas[pos] = pas.get(pos, 0)+c

        tss_pos = [min(tss), max(tss)]
        if tss_pos[1]-tss_pos[0] < smooth_window:
            tss_pos[0] -= (smooth_window + tss_pos[0]-tss_pos[1] - 1)
        pas_pos = [min(pas), max(pas)]
        if pas_pos[1]-pas_pos[0] < smooth_window:
            pas_pos[0] -= (smooth_window + pas_pos[0]-pas_pos[1] - 1)
        tss = [tss.get(pos, 0) for pos in range(tss_pos[0], tss_pos[1]+1)]
        pas = [pas.get(pos, 0) for pos in range(pas_pos[0], pas_pos[1]+1)]
        # smooth profiles and find maxima
        tss_smooth = smooth(np.array(tss), smooth_window)
        pas_smooth = smooth(np.array(pas), smooth_window)
        # at least half of smooth_window reads required to call a peak
        # minimal distance between peaks is > ~ smooth_window
        # rel_prominence=1 -> smaller peak must have twice the hight of valley to call two peaks
        tss_peaks, _ = find_peaks(np.log2(tss_smooth+1), prominence=(rel_prominence, None))
        tss_peak_pos = tss_peaks+tss_pos[0]-1
        pas_peaks, _ = find_peaks(np.log2(pas_smooth+1), prominence=(rel_prominence, None))
        pas_peak_pos = pas_peaks+pas_pos[0]-1

        # find transcripts with common first/last splice site
        first_junction = {}
        last_junction = {}
        for trid, tr in enumerate(self.transcripts):
            first_junction.setdefault(tr['exons'][0][1], []).append(trid)
            last_junction.setdefault(tr['exons'][-1][0], []).append(trid)
        # first / last junction with respect to direction of transcription
        if self.strand == '-':
            first_junction, last_junction = last_junction, first_junction
        # for each site, find consistant "peaks" TSS/PAS
        # if none found use median of all read starts
        for junction_pos, tr_ids in first_junction.items():
            profile = {}
            for trid in tr_ids:
                for sa_tss in self.transcripts[trid]['TSS'].values():
                    for pos, c in sa_tss.items():
                        profile[pos] = profile.get(pos, 0)+c
            quantiles = get_quantiles(sorted(profile.items()), [search_range[0], .5, search_range[1]])
            # one/ several peaks within base range? -> quantify by next read_start
            # else use median
            ol_peaks = [p for p in tss_peak_pos if quantiles[0] < p <= quantiles[-1]]
            if not ol_peaks:
                ol_peaks = [quantiles[1]]
            for trid in tr_ids:
                tr = self.transcripts[trid]
                tr['TSS_unified'] = {}
                for sa, sa_tss in tr['TSS'].items():
                    tss_unified = {}
                    for pos, c in sa_tss.items():  # for each read start position, find closest peak
                        next_peak = min((p for p in ol_peaks if cmp_dist(junction_pos, p, min_dist=3) == strand),
                                        default=pos, key=lambda x: abs(x-pos))
                        tss_unified[next_peak] = tss_unified.get(next_peak, 0)+c
                    tr['TSS_unified'][sa] = tss_unified
        # same for PAS
        for junction_pos, tr_ids in last_junction.items():
            profile = {}
            for trid in tr_ids:
                for sa_pas in self.transcripts[trid]['PAS'].values():
                    for pos, c in sa_pas.items():
                        profile[pos] = profile.get(pos, 0)+c
            quantiles = get_quantiles(sorted(profile.items()), [search_range[0], .5, search_range[1]])
            # one/ several peaks within base range? -> quantify by next read_start
            # else use median
            ol_peaks = [p for p in pas_peak_pos if quantiles[0] < p <= quantiles[-1]]
            if not ol_peaks:
                ol_peaks = [quantiles[1]]
            for trid in tr_ids:
                tr = self.transcripts[trid]
                tr['PAS_unified'] = {}
                for sa, sa_pas in tr['PAS'].items():
                    pas_unified = {}
                    for pos, c in sa_pas.items():
                        next_peak = min((p for p in ol_peaks if cmp_dist(p, junction_pos, min_dist=3) == strand),
                                        default=pos, key=lambda x: abs(x-pos))
                        pas_unified[next_peak] = pas_unified.get(next_peak, 0)+c
                    tr['PAS_unified'][sa] = pas_unified
        for tr in self.transcripts:
            # find the most common tss/pas per transcript, and set the exon boundaries
            sum_tss = {}
            sum_pas = {}
            start = end = max_tss = max_pas = 0
            for sa_tss in tr['TSS_unified'].values():
                for pos, cov in sa_tss.items():
                    sum_tss[pos] = sum_tss.get(pos, 0)+cov
            for pos, cov in sum_tss.items():
                if cov > max_tss:
                    max_tss = cov
                    start = pos
            for sa_pas in tr['PAS_unified'].values():
                for pos, cov in sa_pas.items():
                    sum_pas[pos] = sum_pas.get(pos, 0)+cov
            for pos, cov in sum_pas.items():
                if cov > max_pas:
                    max_pas = cov
                    end = pos
            if self.strand == '-':
                start, end = end, start
            if start >= end:  # for monoexons this may happen in rare situations
                assert len(tr['exons']) == 1
                tr['TSS_unified'] = None
                tr['PAS_unified'] = None
            else:
                try:
                    # issues if the new exon start is behind the exon end
                    assert start < tr['exons'][0][1] or len(tr['exons']) == 1, 'error unifying %s: %s>=%s' % (tr["exons"], start, tr['exons'][0][1])
                    tr['exons'][0][0] = start
                    assert end > tr['exons'][-1][0] or len(tr['exons']) == 1, 'error unifying %s: %s<=%s' % (tr["exons"], end, tr['exons'][-1][0])
                    tr['exons'][-1][1] = end
                except AssertionError:
                    logger.error('%s TSS= %s, PAS=%s -> TSS_unified= %s, PAS_unified=%s', self, tr['TSS'], tr['PAS'],  tr['TSS_unified'], tr['PAS_unified'])
                    raise


def _coding_len(exons, cds):
    coding_len = [0, 0, 0]
    state = 0
    for e in exons:
        if state < 2 and e[1] >= cds[state]:
            coding_len[state] += cds[state] - e[0]
            if state == 0 and cds[1] <= e[1]:  # special case: CDS start and end in same exon
                coding_len[1] = cds[1] - cds[0]
                coding_len[2] = e[1] - cds[1]
                state += 2
            else:
                coding_len[state + 1] = e[1] - cds[state]
                state += 1
        else:
            coding_len[state] += e[1] - e[0]
    return coding_len


def repeat_len(seq1, seq2, wobble, max_mm):
    ''' Calcluate direct repeat length between seq1 and seq2
    '''
    score = [0]*(2*wobble+1)
    delta = int(len(seq1)/2-wobble)
    for w in range(2*wobble+1):  # wobble
        s1 = seq1[w:len(seq1)-(2*wobble-w)]
        s2 = seq2[wobble:len(seq2)-wobble]
        align = [a == b for a, b in zip(s1, s2)]
        score_left = find_runlength(reversed(align[:delta]), max_mm)
        score_right = find_runlength(align[delta:], max_mm)
        score[w] = max([score_left[fmm]+score_right[max_mm-fmm] for fmm in range(max_mm+1)])
    return max(score)


def find_runlength(align, max_mm):
    '''Find the runlength, e.g. the number of True in the list before the max_mm+1 False occur.
    '''
    score = [0]*(max_mm+1)
    mm = 0
    for a in align:
        if not a:
            mm += 1
            if mm > max_mm:
                return score
            score[mm] = score[mm-1]
        else:
            score[mm] += 1
    for i in range(mm+1, max_mm+1):
        score[i] = score[i-1]
    return score
