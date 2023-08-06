import numpy as np
# from numpy.lib.function_base import percentile, quantile
import pandas as pd
from os import path
from intervaltree import IntervalTree, Interval
from collections.abc import Iterable
from collections import Counter
from pysam import TabixFile, AlignmentFile, FastaFile
from tqdm import tqdm
from contextlib import ExitStack
from .short_read import Coverage
from ._utils import junctions_from_cigar, splice_identical, is_same_gene, has_overlap, get_overlap, pairwise, \
    cigar_string2tuples, rc, get_intersects, _find_splice_sites, _get_overlap, get_quantiles  # , _get_exonic_region
from .gene import Gene
from .decorators import experimental
import logging
import gzip as gziplib
from ._transcriptome_filter import SPLICE_CATEGORY

logger = logging.getLogger('isotools')

# io functions for the transcriptome class


def add_short_read_coverage(self, bam_files, load=False):
    '''Adds short read coverage to the genes.

    This does, by default (e.g. if load==False), this method does not actually read the bams,
    but import for each gene is done at first access.

    :param bam_files: A dict with the sample names as keys, and the path to aligned short reads in bam format as values.
    :param load: If True, the coveage of all genes is imported. WARNING: this may take a long time.'''
    self.infos.setdefault('short_reads', pd.DataFrame(columns=['name', 'file'], dtype='object'))

    bam_files = {k: v for k, v in bam_files.items() if k not in self.infos['short_reads']['name']}
    self.infos['short_reads'] = pd.concat([self.infos['short_reads'],
                                           pd.DataFrame({'name': bam_files.keys(), 'file': bam_files.values()})],
                                          ignore_index=True)
    if load:  # when loading coverage for all genes keep the filehandle open, hopefully a bit faster
        for i, bamfile in enumerate(self.infos['short_reads'].file):
            logger.info('Adding short read coverag from %s', bamfile)
            with AlignmentFile(bamfile, "rb") as align:
                for g in tqdm(self):
                    g.data.setdefault('short_reads', list())
                    if len(g.data['short_reads']) == i:
                        g.data['short_reads'].append(Coverage.from_alignment(align, g))


def remove_short_read_coverage(self):
    '''Removes short read coverage.

    Removes all short read coverage information from self.'''

    if 'short_reads' in self.infos:
        del self.infos['short_reads']
        for g in self:
            if 'short_reads' in g:
                del self.data['short_reads']
    else:
        logger.warning('No short read coverage to remove')


@experimental
def remove_samples(self, sample_names):
    ''' Removes samples from the dataset.

    :params sample_names: A list of sample names to remove.'''

    if isinstance(sample_names, str):
        sample_names = [sample_names]
    assert all(s in self.samples for s in sample_names), 'Did not find all samples to remvoe in dataset'
    sample_table = self.sample_table
    rm_idx = sample_table.index[sample_table.name.isin(sample_names)]
    sample_table = sample_table.drop(index=sample_table.index[rm_idx])
    for g in self:
        remove_tr = []
        for i, tr in enumerate(g.transcripts):
            if any(s in tr['coverage'] for s in sample_names):
                tr['coverage'] = {s: cov for s, cov in tr['coverage'].items() if s not in sample_names}
                if not tr['coverage']:
                    remove_tr.append(i)
        if remove_tr:  # remove the transcripts that is not expressed by remaining samples
            g.data['transcripts'] = [tr for i, tr in enumerate(g.transcripts) if i not in remove_tr]
        g.data['segment_graph'] = None  # gets recomputed on next request
        g.data['coverage'] = None


def add_sample_from_csv(self, coverage_csv_file, transcripts_file, transcript_id_col=None, sample_cov_cols=None, sample_properties=None, add_chromosomes=True,
                        reconstruct_genes=True, fuzzy_junction=0, min_exonic_ref_coverage=.25, sep='\t'):
    '''Imports expressed transcripts from coverage table and gtf/gff file, and adds it to the 'Transcriptome' object.

    Transcript to gene assignment is either taken from the transcript_file, or recreated,
    as specified by the reconstruct_genes parameter.
    In the first case, the genes are then matched to overlapping genes from the reference annotation by gene id.
    In absence of a overlapping gene with same id, the gene is matched by splice junction, and renamed.
    A map reflecting the the renaming is returned as a dictionary.

    :param coverage_csv_file: The name of the csv file with coverage information for all samples to be added.
        The file contains columns unique ids for the transcripts, and one column with the coverage for each sample
    :param transcripts_file: Transcripts to be added to the 'Transcriptome' object, in gtf or gff/gff3 format.
        Gene and transcript ids should correspond to ids provided in the coverage_csv_file.
    :param transcript_id_col: Column name with the transcript ids.
        Alternatively, a list of column names can be provided, in which case the transcript id is concatenated from the provided columns,
        seperated by an underscore ("_"). If not specified, checks for columns 'transcript_id' or ['gene_id', 'transcript_nr'].
    :param sample_cov_cols: Dict with sample names for the new samples as keys, and corresponding coverage column names in coverage_csv_file as values.
        If not specified, a new sample is added for each <name>_coverage column.
    :param sample_properties: Additional properties of the samples, that get added to the sample table, and can be used to group or stratify the samples.
        Can be provided either as a dict with sample names as keys, and the respective properties dicts as the values,
        or as a data frame with a column "name" or with the sample names in the index, and the properties in the additional columns.
    :param add_chromosomes: If True, genes from chromosomes which are not in the Transcriptome yet are added.
    :param reconstruct_genes: If True, transcript gene assignment from gtf is ignored, and transcripts are grouped to genes from scratch.
    :param min_exonic_ref_coverage: Minimal fraction of exonic overlap to assign to reference transcript if no splice junctions match.
        Also applies to mono-exonic transcripts
    :param progress_bar: Show the progress.
    :param sep: Specify the seperator for the coverage_csv_file.
    :return: Dict with map of renamed gene ids.
'''

    cov_tab = pd.read_csv(coverage_csv_file, sep=sep)
    if sample_cov_cols is None:
        sample_cov_cols = {c.replace('_coverage', ''): c for c in cov_tab.columns if '_coverage' in c}
    else:
        assert all(c in cov_tab for c in sample_cov_cols.values()), 'coverage cols missing in %s: %s' % (
            coverage_csv_file, ', '.join(c for c in sample_cov_cols.values() if c not in cov_tab))
    samples = list(sample_cov_cols)

    if transcript_id_col is None:
        if 'transcript_id' in cov_tab.columns:
            pass
        elif 'gene_id' in cov_tab.columns and 'transcript_nr' in cov_tab.columns:
            cov_tab['transcript_id'] = cov_tab.gene_id+'_'+cov_tab.transcript_nr.astype(str)
        else:
            raise ValueError('"transcript_id_col" not specified, and coverage table does not contain "transcript_id", nor "gene_id" and "transcript_nr"')
        transcript_id_col = 'transcript_id'
    elif isinstance(transcript_id_col, list):
        assert all(c in cov_tab for c in transcript_id_col), 'missing specified transcript_id_col'
        cov_tab['transcript_id'] = ['_'.join(str(v) for v in row) for _, row in cov_tab[transcript_id_col].iterrows()]
        transcript_id_col = 'transcript_id'
    else:
        assert transcript_id_col in cov_tab, 'missing specified transcript_id_col'
        cov_tab['transcript_id'] = cov_tab[transcript_id_col]
    known_sa = set(samples).intersection(self.samples)
    assert transcript_id_col == 'transcript_id'  # could be optimized, but code is easier when the id column always is transcript_id
    assert not known_sa, 'Attempt to add known samples: %s' % known_sa
    # cov_tab.set_index('transcript_id')
    # assert cov_tab.index.is_unique, 'ambigous transcript ids in %s' % coverage_csv_file
    # check sample properties
    if sample_properties is None:
        sample_properties = {sa: {'group': sa} for sa in samples}
    elif isinstance(sample_properties, pd.DataFrame):
        if 'name' in sample_properties:
            sample_properties = sample_properties.set_index('name')
        sample_properties = {sa: {k: v for k, v in row.items() if k not in {'file', 'nonchimeric_reads', 'chimeric_reads'}}
                             for sa, row in sample_properties.iterrows()}
    assert all(sa in sample_properties for sa in samples), 'missing sample_properties for samples %s' % ', '.join(
        (sa for sa in samples if sa not in sample_properties))
    for sa in sample_properties:
        sample_properties[sa].setdefault('group', sa)

    logger.info('adding samples "%s" from csv', '", "'.join(samples))
    # consider chromosomes not in the referernce?
    if add_chromosomes:
        chromosomes = None
    else:
        chromosomes = self.chromosomes

    file_format = path.splitext(transcripts_file)[1].lstrip('.')
    if file_format == 'gz':
        file_format = path.splitext(transcripts_file[:-3])[1].lstrip('.')
    if file_format == 'gtf':
        exons, transcripts, gene_infos, cds_start, cds_stop, skipped = _read_gtf_file(transcripts_file, chromosomes=chromosomes)
    elif file_format in ('gff', 'gff3'):  # gff/gff3
        exons, transcripts, gene_infos, cds_start, cds_stop, skipped = _read_gff_file(transcripts_file, chromosomes=chromosomes)
    else:
        logger.warning('unknown file format %s of the transcriptome file', file_format)

    logger.debug('sorting exon positions...')
    for tid in exons:
        exons[tid].sort()

    if 'gene_id' not in cov_tab:
        gene_id_dict = {tid: gid for gid, tids in transcripts.items() for tid in tids}
        try:
            cov_tab['gene_id'] = [gene_id_dict[tid] for tid in cov_tab.transcript_id]
        except KeyError as e:
            logger.warning('transcript_id %s from csv file not found in gtf.' % e.args[0])
    if 'chr' not in cov_tab:
        chrom_dict = {gid: chrom for chrom, gids in gene_infos.items() for gid in gids}
        try:
            cov_tab['chr'] = [chrom_dict[gid] for gid in cov_tab.gene_id]
        except KeyError as e:
            logger.warning('gene_id %s from csv file not found in gtf.', e.args[0])

    used_transcripts = set()
    for _, row in cov_tab.iterrows():
        if chromosomes is not None and row.chr not in chromosomes:
            continue
        if all(row[c] == 0 for c in sample_cov_cols.values()):
            continue
        try:
            assert row.transcript_id not in used_transcripts
            tr = transcripts[row.gene_id][row.transcript_id]
            tr['transcript_id'] = row.transcript_id
            tr['exons'] = sorted([list(e) for e in exons[row.transcript_id]])  # needs to be mutable
            tr['coverage'] = {sa: row[sample_cov_cols[sa]] for sa in samples if row[sample_cov_cols[sa]] > 0}
            tr['strand'] = gene_infos[row.chr][row.gene_id][0]['strand']  # gene_infos is a 3 tuple (info, start, end)
            tr['TSS'] = {sa: {tr['exons'][0][0]: row[sample_cov_cols[sa]]} for sa in samples if row[sample_cov_cols[sa]] > 0}
            tr['PAS'] = {sa: {tr['exons'][-1][1]: row[sample_cov_cols[sa]]} for sa in samples if row[sample_cov_cols[sa]] > 0}
            if tr['strand'] == '-':
                tr['TSS'], tr['PAS'] = tr['PAS'], tr['TSS']
            used_transcripts.add(row.transcript_id)
        except KeyError as e:
            logger.warning('skipping transcript %s from gene %s, missing infos in gtf: %s', row.transcript_id, row.gene_id, e.args[0])
        except AssertionError:
            logger.warning('skipping transcript %s from gene %s: duplicate transcript id', row.transcript_id, row.gene_id)
    id_map = {}
    novel_prefix = 'PB_novel_'
    if reconstruct_genes:
        # this approach ignores gene structure, and reassigns transcripts
        novel = {}
        for _, row in cov_tab.iterrows():
            if row.transcript_id not in used_transcripts:
                continue
            tr = transcripts[row.gene_id][row.transcript_id]
            gene = _add_sample_transcript(self, tr, row.chr, fuzzy_junction, min_exonic_ref_coverage)

            if gene is None:
                tr['_original_ids'] = (row.gene_id, row.transcript_id)
                novel.setdefault(row.chr, []).append(Interval(tr['exons'][0][0], tr['exons'][-1][1], tr))
            elif gene.id != row.gene_id:
                id_map.setdefault(row.gene_id, {})[row.transcript_id] = gene.id
        for chrom in novel:
            novel_genes = _add_novel_genes(self, IntervalTree(novel[chrom]), chrom, gene_prefix=novel_prefix)
            for novel_g in novel_genes:
                for novel_tr in novel_g.transcripts:
                    import_id = novel_tr.pop('_original_ids')
                    if novel_g.id != import_id[0]:
                        id_map.setdefault(import_id[0], {})[import_id[1]] = novel_g.id
    else:
        # use gene structure from gtf

        for chrom in gene_infos:
            for gid, (g, start, end) in gene_infos[chrom].items():
                # only transcripts with coverage
                import_id = g['ID']
                tr_list = [tr for trid, tr in transcripts[gid].items() if trid in used_transcripts]
                # find best matching overlapping ref gene
                gene = _add_sample_gene(self, start, end, g, tr_list, chrom, novel_prefix)
                if import_id != gene.id:
                    id_map[import_id] = gene.id
    # todo: extend sample_table
    for sa in samples:
        sample_properties[sa].update({'name': sa, 'file': coverage_csv_file, 'nonchimeric_reads': cov_tab[sample_cov_cols[sa]].sum(), 'chimeric_reads': 0})
        # self.infos['sample_table'] = self.sample_table.append(sample_properties[sa], ignore_index=True)
        self.infos['sample_table'] = pd.concat([self.sample_table, pd.DataFrame([sample_properties[sa]])])

    self.make_index()
    return id_map


def add_sample_from_bam(self, fn, sample_name=None, barcode_file=None, fuzzy_junction=5, add_chromosomes=True, min_mapqual=0,
                        min_align_fraction=.75, chimeric_mincov=2, min_exonic_ref_coverage=.25, use_satag=False, save_readnames=False, progress_bar=True,
                        **kwargs):
    '''Imports expressed transcripts from bam and adds it to the 'Transcriptome' object.

    :param fn: The bam filename of the new sample
    :param sample_name: Name of the new sample. If specified, all reads are assumed to belong to this sample.
    :param barcode_file: For barcoded samples, a file with assignment of sequencing barcodes to sample names.
        This file should be a tab seperated text file with two columns: the barcode and the sample name
        Barcodes not listed in this file will be ignored.
        If sample_name is specified in addition to bacode_file, it will be used as a prefix.
        Barcodes will be read from the XC tag of the bam file.
    :param fuzzy_junction: maximum size for fuzzy junction correction
    :param add_chromosomes: If True, genes from chromosomes which are not in the Transcriptome yet are added.
    :param min_mapqual: Minimum mapping quality of the read to be considdered.
        A mapping quality of 0 usually means ambigous alignment.
    :param min_align_fraction: Minimum fraction of the read sequence matching the reference.
    :param chimeric_mincov: Minimum number of reads for a chimeric transcript to be considered
    :param min_exonic_ref_coverage: Minimal fraction of exonic overlap to assign to reference transcript if no splice junctions match.
        Also applies to mono-exonic transcripts
    :param use_satag: If True, import secondary alignments (of chimeric alignments) from the SA tag.
        This should only be specified if the secondary alignment is not reported in a seperate bam entry.
    :param save_readnames: Save a list of the readnames, that contributed to the transcript.
    :param progress_bar: Show the progress.
    :param kwargs: Additional keyword arugments are added to the sample table.'''

    # todo: one alignment may contain several samples - this is not supported at the moment
    if barcode_file is None:
        assert sample_name is not None, 'Neither sample_name nor barcode_file was specified.'
        assert sample_name not in self.samples, 'sample %s is already in the data set.' % sample_name
        logger.info('adding sample %s from file %s', sample_name, fn)
        barcodes = {}
    else:
        # read the barcode file
        barcodes = pd.read_csv(barcode_file, sep='\t', names=['bc', 'name'], index_col='bc')['name']
        if sample_name is not None:
            barcodes = barcodes.apply(lambda x: '{}_{}'.format(sample_name, x))
        barcodes = barcodes.to_dict()
        assert all(sa not in self.samples for sa in barcodes), \
            'samples %s are already in the data set.' % ', '.join(sa for sa in barcodes if sa in self.samples)
        logger.info('adding %s transcriptomes in %s groups as specified in %s from file %s',
                    len(set(barcodes.keys())), len(set(barcodes.values())), barcode_file, fn)
        barcodes.update({rc(k): v for k, v in barcodes.items()})  # add reverse complement

    kwargs['file'] = fn
    skip_bc = 0
    partial_count = 0
    # genome_fh=FastaFile(genome_fn) if genome_fn is not None else None
    with AlignmentFile(fn, "rb") as align:
        if add_chromosomes:
            chromosomes = align.references
        else:
            chromosomes = self.chromosomes
        stats = align.get_index_statistics()
        # try catch if sam/ no index /not pacbio?
        total_alignments = sum([s.mapped for s in stats if s.contig in chromosomes])
        sample_nc_reads = dict()
        unmapped = n_secondary = n_lowqual = 0
        total_nc_reads_chr = {}
        chimeric = dict()

        with tqdm(total=total_alignments, unit='reads', unit_scale=True, disable=not progress_bar) as pbar:

            for chrom in chromosomes:  # todo: potential issue here - secondary/chimeric alignments to non listed chromosomes are ignored
                total_nc_reads_chr[chrom] = dict()
                pbar.set_postfix(chr=chrom)
                # transcripts=IntervalTree()
                # novel=IntervalTree()
                chr_len = align.get_reference_length(chrom)
                transcripts = IntervalArray(chr_len)  # intervaltree was pretty slow for this context
                novel = IntervalArray(chr_len)
                n_reads = 0
                for read in align.fetch(chrom):
                    n_reads += 1
                    pbar.update(.5)
                    if read.flag & 0x4:  # unmapped
                        unmapped += 1
                        continue
                    if read.flag & 0x700:  # not primary alignment or failed qual check or PCR duplicate
                        n_secondary += 1
                        continue  # use only primary alignments
                    if read.mapping_quality < min_mapqual:  # Mapping quality of 0 usually means ambigous mapping.
                        n_lowqual += 1
                        continue
                    tags = dict(read.tags)
                    if barcodes:
                        if 'XC' not in tags or tags['XC'] not in barcodes:
                            skip_bc += 1
                            continue
                    s_name = sample_name if not barcodes else barcodes[tags['XC']]
                    strand = '-' if read.is_reverse else '+'
                    exons = junctions_from_cigar(read.cigartuples, read.reference_start)
                    tr_range = (exons[0][0], exons[-1][1])
                    if tr_range[0] < 0 or tr_range[1] > chr_len:
                        logger.error('Alignment outside chromosome range: transcript at %s for chromosome %s of length %s', tr_range, chrom, chr_len)
                        continue
                    if 'is' in tags:
                        cov = tags['is']  # number of actual reads supporting this transcript
                    else:
                        cov = 1

                    if 'SA' in tags or read.flag & 0x800:  # part of a chimeric alignment
                        if chimeric_mincov > 0:  # otherwise ignore chimeric read
                            chimeric.setdefault(read.query_name, [{s_name: cov}, []])
                            assert chimeric[read.query_name][0][s_name] == cov, \
                                'error in bam: parts of chimeric alignment for read %s has different coverage information %s != %s' % (
                                    read.query_name, chimeric[read.query_name][0], cov)
                            chimeric[read.query_name][1].append([chrom, strand, exons, aligned_part(read.cigartuples, read.is_reverse), None])
                            if use_satag and 'SA' in tags:
                                for snd_align in (sa.split(',') for sa in tags['SA'].split(';') if sa):
                                    snd_cigartuples = cigar_string2tuples(snd_align[3])
                                    snd_exons = junctions_from_cigar(snd_cigartuples, int(snd_align[1]))
                                    chimeric[read.query_name][1].append(
                                        [snd_align[0], snd_align[2], snd_exons, aligned_part(snd_cigartuples, snd_align[2] == '-'), None])
                                    # logging.debug(chimeric[read.query_name])
                        continue
                    try:
                        # if edit distance becomes large relative to read length, skip the alignment
                        if min_align_fraction > 0 and (1 - tags['NM'] / read.query_length) < min_align_fraction:
                            partial_count += 1
                            continue
                    except KeyError:
                        logging.warning('min_align_fraction set > 0 (%s), but reads found without "NM" tag. Setting min_align_fraction to 0',
                                        min_align_fraction)
                        min_align_fraction = 0

                    total_nc_reads_chr[chrom].setdefault(s_name, 0)
                    total_nc_reads_chr[chrom][s_name] += cov
                    for tr_interval in transcripts.overlap(*tr_range):  # did we see this transcript already?
                        if tr_interval.data['strand'] != strand:
                            continue
                        if splice_identical(exons, tr_interval.data['exons']):
                            tr = tr_interval.data
                            tr.setdefault('range', {}).setdefault(tr_range, 0)
                            tr['range'][tr_range] += cov
                            if save_readnames:
                                tr['reads'].append(read.query_name)
                            break
                    else:
                        tr = {'exons': exons, 'range': {tr_range: cov}, 'strand': strand}
                        if barcodes:
                            tr['bc_group'] = barcodes[tags['XC']]
                        if save_readnames:
                            tr['reads'] = [read.query_name]
                        transcripts.add(Interval(*tr_range, tr))
                    # if genome_fh is not None:
                    #    mutations=get_mutations(read.cigartuples, read.query_sequence, genome_fh, chrom,read.reference_start,read.query_qualities)
                    #    for pos,ref,alt,qual in mutations:
                    #        tr.setdefault('mutations',{}).setdefault(sample_name,{}).setdefault(pos,{'ref':ref}).setdefault(alt,[0,[]])
                    #        tr['mutations'][sample_name][pos][alt][0]+=cov
                    #        if qual:
                    #            tr['mutations'][sample_name][pos][alt][1].append(qual) #assuming the quality already accounts for cov>1

                    if 4 in read.cigartuples:  # clipping
                        s_name = sample_name if not barcodes else barcodes[tags['XC']]
                        clip = get_clipping(read.cigartuples, read.reference_start)
                        tr.setdefault('clipping', {}).setdefault(s_name, {}).setdefault(clip, 0)
                        tr['clipping'][s_name][clip] += cov
                for tr_interval in transcripts:
                    tr = tr_interval.data
                    tr_ranges = tr.pop('range')
                    # tr_ranges=tr['range']
                    starts, ends = {}, {}
                    for r, cov in tr_ranges.items():
                        starts[r[0]] = starts.get(r[0], 0) + cov
                        ends[r[1]] = ends.get(r[1], 0) + cov
                    # get the median TSS/PAS
                    tr['exons'][0][0] = get_quantiles(starts.items(), [0.5])[0]
                    tr['exons'][-1][1] = get_quantiles(ends.items(), [0.5])[0]
                    cov = sum(tr_ranges.values())
                    s_name = tr.get('bc_group', sample_name)
                    tr['coverage'] = {s_name: cov}
                    tr['TSS'] = {s_name: starts if tr['strand'] == '+' else ends}
                    tr['PAS'] = {s_name: starts if tr['strand'] == '-' else ends}

                    gene = _add_sample_transcript(self, tr, chrom, fuzzy_junction, min_exonic_ref_coverage)
                    if gene is None:
                        novel.add(tr_interval)
                    else:
                        _ = tr.pop('bc_group', None)
                    n_reads -= cov
                    pbar.update(cov / 2)
                _ = _add_novel_genes(self, novel, chrom)

                pbar.update(n_reads / 2)  # some reads are not processed here, add them to the progress: chimeric, unmapped, secondary alignment
                # logger.debug(f'imported {total_nc_reads_chr[chrom]} nonchimeric reads for {chrom}')
                for sa, nc_reads in total_nc_reads_chr[chrom].items():
                    sample_nc_reads[sa] = sample_nc_reads.get(sa, 0) + nc_reads
    if partial_count:
        logger.info('skipped %s reads aligned fraction of less than %s.', partial_count, min_align_fraction)
    if skip_bc:
        logger.warning('skipped %s reads with barcodes not found in the provided list.', skip_bc)
    if n_secondary > 0:
        logger.info('skipped %s secondary alignments (0x100), alignment that failed quality check (0x200) or PCR duplicates (0x400)', n_secondary)
    if unmapped > 0:
        logger.info('ignored %s reads marked as unaligned', unmapped)
    if n_lowqual > 0:
        logger.info('ignored %s reads with mapping quality < %s', n_lowqual, min_mapqual)

    # merge chimeric reads and assign gene names

    n_chimeric = dict()
    # split up chimeric reads in actually chimeric and long introns (non_chimeric)
    # chimeric are grouped by breakpoint (bp->{readname->(chrom, strand, exons)})
    chim, non_chimeric = _check_chimeric(chimeric)
    # sample_nc_reads[sa]

    n_chimeric = _add_chimeric(self, chim, chimeric_mincov, min_exonic_ref_coverage)
    n_long_intron = {}
    for nc_cov_dict, _, _ in non_chimeric.values():
        for sa, nc_cov in nc_cov_dict.items():
            n_long_intron[sa] = n_long_intron.get(sa, 0) + nc_cov
            sample_nc_reads[sa] = sample_nc_reads.get(sa, 0) + nc_cov
    chim_ignored = sum(len(chim) for chim in chimeric.values()) - sum(n_chimeric.values())
    if chim_ignored > 0:
        logger.info('ignoring %s chimeric alignments with less than %s reads', chim_ignored, chimeric_mincov)
    chained_msg = '' if not sum(n_long_intron.values()) else f' (including  {sum(n_long_intron.values())} chained chimeric alignments)'
    chimeric_msg = '' if sum(n_chimeric.values()) == 0 else f' and {sum(n_chimeric.values())} chimeric reads with coverage of at least {chimeric_mincov}'
    logger.info('imported %s nonchimeric reads%s%s.', sum(sample_nc_reads.values()), chained_msg, chimeric_msg)

    for readname, (cov, (chrom, strand, exons, _, _), introns) in non_chimeric.items():
        novel = dict()
        try:
            tss, pas = (exons[0][0], exons[-1][1]) if strand == '+' else (exons[-1][1], exons[0][0])
            tr = {'exons': exons, 'coverage': cov, 'TSS': {sa: {tss: c} for sa, c in cov.items()}, 'PAS': {sa: {pas: c} for sa, c in cov.items()},
                  'strand': strand, 'chr': chrom, 'long_intron_chimeric': introns}
            if save_readnames:
                tr['reads'] = {s_name: [readname]}
        except BaseException:
            logger.error('\n\n-->%s\n\n', (exons[0][0], exons[-1][1]) if strand == "+" else (exons[-1][1], exons[0][0]))
            raise
        gene = _add_sample_transcript(self, tr, chrom, fuzzy_junction, min_exonic_ref_coverage)  # tr is not updated
        if gene is None:
            novel.setdefault(chrom, []).append(tr)
        for chrom in novel:
            _ = _add_novel_genes(self, IntervalTree(Interval(tr['exons'][0][0], tr['exons'][-1][1], tr) for tr in novel[chrom]), chrom)

        # self.infos.setdefault('chimeric',{})[s_name]=chimeric # save all chimeric reads (for debugging)
    for g in self:
        if 'coverage' in g.data and g.data['coverage'] is not None:  # still valid splice graphs no new transcripts - add a row of zeros to coveage
            g._set_coverage()
    for s_name in sample_nc_reads:
        kwargs['chimeric_reads'] = n_chimeric.get(s_name, 0)
        kwargs['nonchimeric_reads'] = sample_nc_reads.get(s_name, 0)
        kwargs['name'] = s_name
        # self.infos['sample_table'] = self.sample_table.append(kwargs, ignore_index=True)
        self.infos['sample_table'] = pd.concat([self.sample_table, pd.DataFrame([kwargs])])
    self.make_index()
    return total_nc_reads_chr


def _add_chimeric(t, new_chimeric, min_cov, min_exonic_ref_coverage):
    ''' add new chimeric transcripts to transcriptome, if covered by > min_cov reads
    '''
    total = {}
    for new_bp, new_chim_dict in new_chimeric.items():
        n_reads = {}
        for cov_all, _ in new_chim_dict.values():
            for sa, cov in cov_all.items():
                n_reads[sa] = n_reads.get(sa, 0)+cov
        n_reads = {sa: cov for sa, cov in n_reads.items() if cov >= min_cov}
        if not n_reads:
            continue
        for sa in n_reads:
            total[sa] = total.get(sa, 0) + n_reads[sa]
        for _, new_chim in new_chim_dict.items():  # ignore the readname for now
            # should not contain: long intron, one part only (filtered by check_chimeric function),
            # todo: discard invalid (large overlaps, large gaps)
            # find equivalent chimeric reads
            for found in t.chimeric.setdefault(new_bp, []):
                if all(splice_identical(ch1[2], ch2[2]) for ch1, ch2 in zip(new_chim[1], found[1])):
                    # add coverage
                    for sa in n_reads:
                        found[0][sa] = found[0].get(sa, 0) + n_reads[sa]
                    # adjust start using the maximum range
                    # this part deviates from normal transcripts, where the median tss/pas is used
                    if found[1][0][1] == '+':  # strand of first part
                        found[1][0][2][0][0] = min(found[1][0][2][0][0], new_chim[1][0][2][0][0])
                    else:
                        found[1][0][2][0][1] = max(found[1][0][2][0][1], new_chim[1][0][2][0][1])
                    # adjust end
                    if found[1][-1][1] == '+':  # strand of last part
                        found[1][-1][2][-1][1] = max(found[1][-1][2][-1][1], new_chim[1][-1][2][-1][1])
                    else:
                        found[1][-1][2][-1][0] = min(found[1][-1][2][-1][0], new_chim[1][-1][2][-1][0])
                    break
            else:  # not seen
                t.chimeric[new_bp].append(new_chim)
                for part in new_chim[1]:
                    if part[0] in t.data:
                        genes_ol = [g for g in t.data[part[0]][part[2][0][0]: part[2][-1][1]] if g.strand == part[1]]
                        g, _, _ = _find_matching_gene(genes_ol, part[2], min_exonic_ref_coverage)  # take the best - ignore other hits here
                        if g is not None:
                            part[4] = g.name
                            g.data.setdefault('chimeric', {})[new_bp] = t.chimeric[new_bp]
    return total


def _breakpoints(chimeric):
    ''' gets chimeric aligment as a list and returns list of breakpoints.
        each breakpoint is a tuple of (chr1, strand1, pos1,  chr2,strand2,pos2)
    '''
    return tuple((a[0], a[1], a[2][-1][1] if a[1] == '+' else a[2][0][0],
                  b[0], b[1], b[2][0][0] if b[1] == '+' else b[2][-1][1])
                 for a, b in pairwise(chimeric))


def _check_chimeric(chimeric):
    ''' prepare the chimeric reads:
        1) sort parts according to read order
        2) compute breakpoints
        3) check if the chimeric read is actually a long introns - return list as nonchimeric
        4) sort into dict by breakpoint - return dict as chimeric

        chimeric[0] is the coverage dict
        chimeric[1] is a list of tuples: chrom,strand,exons,[aligned start, end] '''

    chimeric_dict = {}
    non_chimeric = {}
    skip = 0
    for readname, new_chim in chimeric.items():
        if len(new_chim[1]) < 2:
            skip += sum(new_chim[0].values())
            continue
        merged_introns = []

        # 1) sort
        new_chim[1].sort(key=lambda x: x[3][1])  # sort by end of aligned part
        # 2) compute breakpoints
        bpts = _breakpoints(new_chim[1])  # compute breakpoints
        # 3) check if long intron alignment splits
        merge = [i for i, bp in enumerate(bpts) if
                 bp[0] == bp[3] and  # same chr
                 bp[1] == bp[4] and  # same strand,
                 0 < (bp[5] - bp[2] if bp[1] == '+' else bp[2] - bp[5]) < 1e6]  # max 1mb gap -> long intron
        # todo: also check that the aligned parts have not big gap or overlap
        if merge:
            # new_chim[1]
            intron = 0
            for i, part in enumerate(new_chim[1]):
                intron += len(part[2])
                if i in merge:
                    merged_introns.append(intron)

            for i in merge:  # part i is merged into part i+1
                if new_chim[1][i][1] == '+':  # merge into next part
                    new_chim[1][i + 1][2] = new_chim[1][i][2] + new_chim[1][i + 1][2]
                    new_chim[1][i + 1][3] = new_chim[1][i][3] + new_chim[1][i + 1][3]
                else:
                    new_chim[1][i + 1][2] = new_chim[1][i + 1][2] + new_chim[1][i][2]
                    new_chim[1][i + 1][3] = new_chim[1][i + 1][3] + new_chim[1][i][3]
            # remove redundant parts (i)
            new_chim[1] = [part for i, part in enumerate(new_chim[1]) if i not in merge]
            bpts = tuple(bp for i, bp in enumerate(bpts) if i not in merge)
        # sort into chimeric (e.g. still breakpoints left) and nonchimeric (only one part and no breakpoints left)
        if bpts:
            chimeric_dict.setdefault(bpts, {})[readname] = new_chim
        else:
            assert len(new_chim[1]) == 1
            # coverage, part(chrom,strand,exons,[aligned start, end]), and "long introns"
            non_chimeric[readname] = [new_chim[0], new_chim[1][0], tuple(merged_introns)]
    if skip:
        logger.warning('ignored %s chimeric alignments with only one part aligned to specified chromosomes.', skip)
    return chimeric_dict, non_chimeric


def _add_sample_gene(t, g_start, g_end, g_infos, tr_list, chrom, novel_prefix):
    '''add new gene to existing gene in chrom - return gene on success and None if no Gene was found.
    For matching transcripts in gene, transcripts are merged. Coverage, tr TSS/PAS need to be reset.
    Otherwise, a new transcripts are added. In this case, splice graph and coverage have to be reset.'''
    if chrom not in t.data:
        for tr in tr_list:
            tr['annotation'] = (4, {'intergenic': []})
        return t._add_novel_gene(chrom, g_start, g_end, g_infos['strand'], {'transcripts': tr_list}, novel_prefix)

    # try matching the gene by id
    try:
        best_gene = t[g_infos['ID']]
        if not best_gene.is_annotated or not has_overlap((best_gene.start, best_gene.end), (g_start, g_end)):
            best_gene = None
        elsefound = []  # todo: to annotate as fusion, we would need to check for uncovered splice sites, and wether other genes cover them
    except KeyError:
        best_gene = None

    if best_gene is None:
        # find best matching reference gene from t
        genes_ol_strand = [g for g in t.data[chrom][g_start: g_end] if g.strand == g_infos['strand']]

        if not genes_ol_strand:
            covered_splice = 0
        else:
            sj = sorted(list({(e1[1], e2[0]) for tr in tr_list for e1, e2 in pairwise(tr['exons'])}))
            splice_sites = np.array([g.ref_segment_graph.find_splice_sites(sj) if g.is_annotated
                                     else _find_splice_sites(sj, g.transcripts) for g in genes_ol_strand])
            sum_ol = splice_sites.sum(1)
            covered_splice = np.max(sum_ol)
        if covered_splice > 0:
            best_idx = np.flatnonzero(sum_ol == covered_splice)
            best_idx = best_idx[0]
            not_in_best = np.where(~splice_sites[best_idx])[0]
            additional = splice_sites[:, not_in_best]  # additional= sites not covered by top gene
            elsefound = [(g.name, not_in_best[a]) for g, a in zip(genes_ol_strand, additional) if a.sum() > 0]  # genes that cover additional splice sites
            # notfound = (splice_sites.sum(0) == 0).nonzero()[0].tolist()  # not covered splice sites
            # tr['novel_splice_sites'] = not_found # cannot be done here, as gene is handled at once. TODO: maybe later?
            best_gene = genes_ol_strand[best_idx]
        else:
            genes_ol_anti = [g for g in t.data[chrom][g_start: g_end] if g.strand != g_infos['strand']]
            for tr in tr_list:
                tr['annotation'] = (4, _get_novel_type(tr['exons'], genes_ol_anti, genes_ol_strand))
            return t._add_novel_gene(chrom, g_start, g_end, g_infos['strand'], {'transcripts': tr_list}, novel_prefix)

    for tr in tr_list:
        for tr2 in best_gene.transcripts:  # check if correction made it identical to existing
            if splice_identical(tr2['exons'], tr['exons']):
                _combine_transcripts(tr2, tr)  # potentially loosing information
                break
        else:
            if best_gene.is_annotated and has_overlap((tr['exons'][0][0], tr['exons'][-1][1]), (best_gene.start, best_gene.end)):
                # potentially problematic: elsefound [(genename, idx),...] idx does not refere to transcript splice site
                try:
                    tr['annotation'] = best_gene.ref_segment_graph.get_alternative_splicing(tr['exons'], elsefound)
                except Exception:
                    logger.error('issue categorizing transcript %s with respect to %s', tr['exons'], str(best_gene))
                    raise
            else:
                genes_ol_strand = [g for g in t.data[chrom][g_start: g_end] if g.strand == g_infos['strand'] and g.is_annotated]
                genes_ol_anti = [g for g in t.data[chrom][g_start: g_end] if g.strand != g_infos['strand'] and g.is_annotated]
                tr['annotation'] = (4, _get_novel_type(tr['exons'], genes_ol_anti, genes_ol_strand))  # actually may overlap other genes...
            best_gene.data.setdefault('transcripts', []).append(tr)
    return best_gene


def _add_sample_transcript(t, tr, chrom,  fuzzy_junction, min_exonic_ref_coverage, genes_ol=None):
    '''add transcript to gene in chrom - return gene on success and None if no Gene was found.
    If matching transcript is found in gene, transcripts are merged. Coverage, tr TSS/PAS need to be reset.
    Otherwise, a new transcript is added. In this case, splice graph and coverage have to be reset.'''

    if chrom not in t.data:
        tr['annotation'] = (4, {'intergenic': []})
        return None
    if genes_ol is None:
        genes_ol = t.data[chrom][tr['exons'][0][0]: tr['exons'][-1][1]]
    genes_ol_strand = [g for g in genes_ol if g.strand == tr['strand']]
    # check if transcript is already there (e.g. from other sample, or in case of long intron chimeric alignments also same sample):
    for g in genes_ol_strand:
        for tr2 in g.transcripts:
            if splice_identical(tr2['exons'], tr['exons']):
                _combine_transcripts(tr2, tr)
                return g
    # we have a new transcript (not seen in this or other samples)
    # check if gene is already there (e.g. from same or other sample):
    g, additional, not_covered = _find_matching_gene(genes_ol_strand, tr['exons'], min_exonic_ref_coverage)
    if g is not None:
        if g.is_annotated:  # check for fuzzy junctions (e.g. same small shift at 5' and 3' compared to reference annotation)
            shifts = g.correct_fuzzy_junctions(tr, fuzzy_junction, modify=True)  # this modifies tr['exons']
            if shifts:
                tr.setdefault('fuzzy_junction', []).append(shifts)  # keep the info, mainly for testing/statistics
                for tr2 in g.transcripts:  # check if correction made it identical to existing
                    if splice_identical(tr2['exons'], tr['exons']):
                        tr2.setdefault('fuzzy_junction', []).append(shifts)  # keep the info, mainly for testing/statistics
                        _combine_transcripts(tr2, tr)
                        return g
            tr['annotation'] = g.ref_segment_graph.get_alternative_splicing(tr['exons'], additional)

            if not_covered:
                tr['novel_splice_sites'] = not_covered  # todo: might be changed by fuzzy junction

            # intersects might have changed due to fuzzy junctions
            # {'sj_i': sj_i, 'base_i':base_i,'category':SPLICE_CATEGORY[altsplice[1]],'subcategory':altsplice[1]}

        else:  # add to existing novel (e.g. not in reference) gene
            start, end = min(tr['exons'][0][0], g.start), max(tr['exons'][-1][1], g.end)
            tr['annotation'] = (4, _get_novel_type(tr['exons'], genes_ol, genes_ol_strand))
            if start < g.start or end > g.end:  # range of the novel gene might have changed
                new_gene = Gene(start, end, g.data, t)
                t.data[chrom].add(new_gene)  # todo: potential issue: in this case two genes may have grown together
                t.data[chrom].remove(g)
                g = new_gene
        # if additional:
        #    tr['annotation']=(4,tr['annotation'][1]) #fusion transcripts... todo: overrule tr['annotation']
        # this transcript is seen for the first time. Asign sample specific attributes to sample name
        # for what in 'coverage', 'TSS', 'PAS':
        #    tr[what] = {sample_name: tr[what]}
        # if 'reads' in tr:
        #    tr['reads'] = {sample_name: tr['reads']}
        g.data.setdefault('transcripts', []).append(tr)
        g.data['segment_graph'] = None  # gets recomputed on next request
        g.data['coverage'] = None
    else:
        # new novel gene
        tr['annotation'] = (4, _get_novel_type(tr['exons'], genes_ol, genes_ol_strand))
    return g


def _combine_transcripts(established, new_tr):
    'merge new_tr into splice identical established transcript'
    try:
        for sample_name in new_tr['coverage']:
            established['coverage'][sample_name] = established['coverage'].get(sample_name, 0) + new_tr['coverage'][sample_name]
        for sample_name in new_tr.get('reads', {}):
            established['reads'].setdefault(sample_name, []).extend(new_tr['reads'])
        for side in 'TSS', 'PAS':
            for sample_name in new_tr[side]:
                for pos, cov in new_tr[side][sample_name].items():
                    established[side].setdefault(sample_name, {}).setdefault(pos, 0)
                    established[side][sample_name][pos] += cov
        # find median tss and pas
        starts = [v for sa in established['TSS'] for v in established['TSS'][sa].items()]
        ends = [v for sa in established['PAS'] for v in established['PAS'][sa].items()]
        if established['strand'] == '-':
            starts, ends = ends, starts
        established['exons'][0][0] = get_quantiles(starts, [0.5])[0]
        established['exons'][-1][1] = get_quantiles(ends, [0.5])[0]
        if 'long_intron_chimeric' in new_tr:
            new_introns = set(new_tr['long_intron_chimeric'])
            established_introns = set(established.get('long_intron_chimeric', set()))
            established['long_intron_chimeric'] = tuple(new_introns.union(established_introns))
    except BaseException:
        logger.error('error when merging %s into %s', new_tr, established)
        raise


def _get_novel_type(exons, genes_ol, genes_ol_strand):
    if len(genes_ol_strand):
        exonic_overlap = {g.id: g.ref_segment_graph.get_overlap(exons) for g in genes_ol_strand if g.is_annotated}
        exonic_overlap_genes = [k for k, v in exonic_overlap.items() if v[0] > 0]
        if len(exonic_overlap_genes) > 0:
            return {'genic genomic': exonic_overlap_genes}
        return {'intronic': [g.name for g in genes_ol_strand]}
    elif len(genes_ol):
        return {'antisense': [g.name for g in genes_ol]}
    else:
        return {'intergenic': []}


def _add_novel_genes(t, novel, chrom, spj_iou_th=0, reg_iou_th=.5, gene_prefix='PB_novel_'):
    '"novel" is a tree of transcript intervals (not Gene objects) ,e.g. from one chromosome, that do not overlap any annotated or unanntoated gene'
    n_novel = t.novel_genes
    idx = {id(tr): i for i, tr in enumerate(novel)}
    novel_gene_list = []
    merge = list()
    for i, tr in enumerate(novel):
        merge.append({tr})
        candidates = [c for c in novel.overlap(tr.begin, tr.end) if c.data['strand'] == tr.data['strand'] and idx[id(c)] < i]
        for c in candidates:
            if c in merge[i]:
                continue
            if is_same_gene(tr.data['exons'], c.data['exons'], spj_iou_th, reg_iou_th):
                # add all transcripts of candidate
                merge[i].update(merge[idx[id(c)]])
        for c in merge[i]:  # update all overlapping (add the current to them)
            merge[idx[id(c)]] = merge[i]

    seen = set()
    for trS in merge:
        if id(trS) in seen:
            continue
        seen.add(id(trS))
        trL = [tr.data for tr in trS]
        strand = trL[0]['strand']
        start = min(tr['exons'][0][0] for tr in trL)
        end = max(tr['exons'][-1][1] for tr in trL)
        assert start < end, 'novel gene with start >= end'
        # for tr in trL:
        #    sample_name = tr.pop('bc_group', sa)
        #    tr['coverage'] = {sample_name: tr['coverage']}
        #    tr['TSS'] = {sample_name: tr['TSS']}
        #    tr['PAS'] = {sample_name: tr['PAS']}
        #    if 'reads' in tr:
        #        tr['reads'] = {sample_name: tr['reads']}
        novel_gene_list.append(t._add_novel_gene(chrom, start, end, strand, {'transcripts': trL}, gene_prefix))
        logging.debug('merging transcripts of novel gene %s: %s', n_novel, trL)
    return novel_gene_list


def _find_matching_gene(genes_ol, exons, min_exon_coverage):
    '''check the splice site intersect of all overlapping genes and return
            1) the gene with most shared splice sites,
            2) names of genes that cover additional splice sites, and
            3) splice sites that are not covered.
        If no splice site is shared (and for mono-exon genes) return the gene with largest exonic overlap
        :param min_exon_coverage: minimum exonic coverage with genes that do not share splice sites to be considered'''
    trlen = sum(e[1]-e[0] for e in exons)
    sj = [(e1[1], e2[0]) for e1, e2 in pairwise(exons)]
    if genes_ol:
        if len(exons) > 1:
            nomatch = np.zeros(len(sj) * 2, dtype=bool)
            splice_sites = np.array([g.ref_segment_graph.find_splice_sites(sj) if g.is_annotated else nomatch for g in genes_ol])
            sum_ol = splice_sites.sum(1)
            # find index of reference gene that covers the most splice sites
            # resolved issue with tie here, missing FSM due to overlappnig gene with extention of FSM transcript
            covered_splice = np.max(sum_ol)
            if covered_splice == 0:  # none found, consider novel genes
                splice_sites = np.array([_find_splice_sites(sj,  g.transcripts) if not g.is_annotated else nomatch for g in genes_ol])
                sum_ol = splice_sites.sum(1)
                covered_splice = np.max(sum_ol)
            if covered_splice > 0:
                best_idx = np.flatnonzero(sum_ol == covered_splice)
                if len(best_idx > 1):  # handle ties
                    # find the transcript with the highest fraction of matching junctions
                    tr_inter = []
                    for idx in best_idx:
                        trlist = genes_ol[idx].ref_transcripts if genes_ol[idx].is_annotated else genes_ol[idx].transcripts
                        tr_intersects = [(get_intersects(exons, tr['exons'])) for tr in trlist]
                        tr_intersects_fraction = [(ji/len(trlist[idx]['exons']), ei) for idx, (ji, ei) in enumerate(tr_intersects)]
                        tr_inter.append(max(tr_intersects_fraction))
                    best_idx = best_idx[tr_inter.index(max(tr_inter))]
                else:
                    best_idx = best_idx[0]
                not_in_best = np.where(~splice_sites[best_idx])[0]
                additional = splice_sites[:, not_in_best]  # additional= sites not covered by top gene
                elsefound = [(g.name, not_in_best[a]) for g, a in zip(genes_ol, additional) if a.sum() > 0]  # genes that cover additional splice sites
                notfound = (splice_sites.sum(0) == 0).nonzero()[0].tolist()  # not covered splice sites
                return genes_ol[best_idx], elsefound, notfound
            # no shared splice sites, return gene with largest overlap
            # first, check reference here:
            # 1) if >50% ol with ref gene -> return best ref gene
            ol = np.array([g.ref_segment_graph.get_overlap(exons)[0] if g.is_annotated else 0 for g in genes_ol])
            best_idx = ol.argmax()
            if ol[best_idx] >= min_exon_coverage * sum(e[1] - e[0] for e in exons):
                return genes_ol[best_idx], None, list(range((len(exons) - 1) * 2))
        else:
            # len(exons)==1 check all ref transcripts for monoexon gene with overlap>=50% (or min_exon_coverage)
            ol = []
            for g in genes_ol:
                ol_g = [get_overlap(exons[0], tr['exons'][0]) for tr in g.ref_transcripts if len(tr['exons']) == 1]
                ol.append(max(ol_g, default=0))
            best_idx = np.argmax(ol)
            if ol[best_idx] >= min_exon_coverage * trlen:
                return genes_ol[best_idx], None, []
        # else return best overlapping novel gene if more than minimum overlap fraction
        ol = [(0, []) if not g.is_annotated else g.ref_segment_graph.get_overlap(exons) for g in genes_ol]
        max_ol_frac = np.array([0 if ol[0] == 0 else max(ol_tr / min(trlen, sum(e[1] - e[0] for e in tr["exons"]))
                                                         for ol_tr, tr in zip(ol[1], g.ref_transcripts)) for g, ol in zip(genes_ol, ol)])
        best_idx = max_ol_frac.argmax()
        if max_ol_frac[best_idx] >= min_exon_coverage:
            return genes_ol[best_idx], None, list(range((len(exons) - 1) * 2))  # none of the junctions are covered
        # else return best overlapping novel gene if more than minimum overlap fraction
        ol = [0 if g.is_annotated else _get_overlap(exons, g.transcripts) for g in genes_ol]
        max_ol_frac = np.array([0 if ol == 0 else ol_gene / trlen for ol_gene in ol])
        best_idx = max_ol_frac.argmax()
        if max_ol_frac[best_idx] >= min_exon_coverage:
            return genes_ol[best_idx], None, list(range((len(exons) - 1) * 2))  # none of the junctions are covered
        # TODO: Issue: order matters here, if more than one novel gene with >50%ol, join them all?)
    return None, None, list(range((len(exons) - 1) * 2))  # none of the junctions are covered


def _read_gtf_file(file_name, chromosomes, infer_genes=False, progress_bar=True):
    exons = dict()  # transcript id -> exons
    transcripts = dict()  # gene_id -> transcripts
    skipped = set()
    gene_infos = dict()  # 4 tuple: info_dict, gene_start, gene_end, fixed_flag==True if start/end are fixed
    inferred_genes = dict()
    cds_start = dict()
    cds_stop = dict()
    # with tqdm(total=path.getsize(file_name), unit_scale=True, unit='B', unit_divisor=1024, disable=not progress_bar) as pbar, TabixFile(file_name) as gtf:
    # for line in gtf.fetch():
    #    file_pos = gtf.tell() >> 16
    #    if pbar.n < file_pos:
    #       pbar.update(file_pos-pbar.n)
    openfun = gziplib.open if file_name.endswith('.gz') else open

    with openfun(file_name, "rt") as gtf:
        for line in gtf:
            if line[0] == '#':  # ignore header lines
                continue
            ls = line.split(sep="\t")
            assert len(ls) == 9, 'unexpected number of fields in gtf line:\n%s' % line
            if chromosomes is not None and ls[0] not in chromosomes:
                logger.debug('skipping line from chr '+ls[0])
                continue
            try:
                info = dict([pair.lstrip().split(maxsplit=1) for pair in ls[8].strip().replace('"', '').split(";") if pair])
            except ValueError:
                logger.error('issue with key value pairs from gtf:\n%s', ls[8])
                raise
            start, end = [int(i) for i in ls[3:5]]
            start -= 1  # to make 0 based
            if ls[2] == "exon":
                # logger.debug(line)
                try:
                    _ = exons.setdefault(info['transcript_id'], list()).append((start, end))
                except KeyError:  # should not happen if GTF is OK
                    logger.error("gtf format error: exon without transcript_id\n%s", line)
                    raise
                if infer_genes and 'gene_id' in info:
                    inferred_genes.setdefault(ls[0], {})
                    if info['gene_id'] not in gene_infos[ls[0]]:  # new gene
                        info['strand'] = ls[6]
                        info['chr'] = ls[0]
                        _set_alias(info, {'ID': ['gene_id']})
                        _set_alias(info, {'name': ['gene_name', 'Name']}, required=False)
                        ref_info = {k: v for k, v in info.items() if k not in Gene.required_infos + ['name']}
                        info = {k: info[k] for k in Gene.required_infos + ['name'] if k in info}
                        info['properties'] = ref_info
                        inferred_genes[ls[0]][info['ID']] = (info, start, end)  # start/end not fixed yet (initially set to exon start end)
                    else:
                        known_info = inferred_genes[ls[0]][info['gene_id']]
                        gene_infos[info['gene_id']] = (known_info[0], min(known_info[1], start), max(known_info[2], end))
                        if 'transcript_id' in info and info['transcript_id'] not in transcripts.setdefault(info['gene_id'], {}):
                            # new transcript
                            tr_info = {k: v for k, v in info.items() if 'transcript' in k and k != 'transcript_id'}
                            transcripts[info["gene_id"]][info["transcript_id"]] = tr_info

            elif ls[2] == 'gene':
                if 'gene_id' not in info:
                    logger.warning("gtf format error: gene without gene_id. Skipping line\n%s", line)
                else:  # overrule potential entries from exon line
                    info['strand'] = ls[6]
                    info['chr'] = ls[0]
                    _set_alias(info, {'ID': ['gene_id']})
                    _set_alias(info, {'name': ['gene_name', 'Name']}, required=False)
                    ref_info = {k: v for k, v in info.items() if k not in Gene.required_infos + ['name']}
                    info = {k: info[k] for k in Gene.required_infos + ['name'] if k in info}
                    info['properties'] = ref_info
                    gene_infos.setdefault(ls[0], {})[info['ID']] = (info, start, end)
            elif ls[2] == 'transcript':  # overrule potential entries from exon line
                try:
                    # keep only transcript related infos (to avoid redundant gene infos)
                    tr_info = {k: v for k, v in info.items() if 'transcript' in k and k != 'transcript_id'}
                    _ = transcripts.setdefault(info["gene_id"], dict())[info["transcript_id"]] = tr_info
                except KeyError:
                    logger.warning("gtf format errror: transcript must have gene_id and transcript_id, skipping line\n%s", line)
            elif ls[2] == 'start_codon' and 'transcript_id' in info:
                cds_start[info['transcript_id']] = end if ls[6] == '-' else start
            elif ls[2] == 'stop_codon' and 'transcript_id' in info:
                cds_stop[info['transcript_id']] = start if ls[6] == '-' else end
            else:
                skipped.add(ls[2])

    return exons, transcripts, gene_infos, cds_start, cds_stop, skipped


def _get_tabix_end(tbx_fh):
    for line in tbx_fh.fetch(tbx_fh.contigs[-1]):
        pass
    end = tbx_fh.tell()
    tbx_fh.seek(0)
    return end


def _read_gff_file(file_name, chromosomes, progress_bar=True):
    exons = dict()  # transcript id -> exons
    transcripts = dict()  # gene_id -> transcripts
    skipped = set()
    genes = dict()
    cds_start = dict()
    cds_stop = dict()
    # takes quite some time... add a progress bar?
    with tqdm(total=path.getsize(file_name), unit_scale=True, unit='B', unit_divisor=1024, disable=not progress_bar) as pbar, TabixFile(file_name) as gff:
        chrom_ids = get_gff_chrom_dict(gff, chromosomes)
        for line in gff.fetch():
            file_pos = gff.tell() >> 16  # the lower 16 bit are the position within the zipped block
            if pbar.n < file_pos:
                pbar.update(file_pos-pbar.n)
            ls = line.split(sep="\t")
            if ls[0] not in chrom_ids:
                continue
            chrom = chrom_ids[ls[0]]
            if chromosomes is not None and chrom not in chromosomes:
                logger.debug('skipping line %s from chr %s', line, chrom)
                continue
            try:
                info = dict([pair.split('=', 1) for pair in ls[8].rstrip(';').split(";")])  # some gff lines end with ';' in gencode 36
            except ValueError:
                logger.warning("GFF format error in infos (should be ; seperated key=value pairs). Skipping line:\n%s", line)
            start, end = [int(i) for i in ls[3:5]]
            start -= 1  # to make 0 based
            if ls[2] == "exon":
                try:
                    gff_id = info['Parent']
                    exons.setdefault(gff_id, list()).append((start, end))
                except KeyError:  # should not happen if GFF is OK
                    logger.warning("GFF format error: no parent found for exon. Skipping line:\n%s", line)
            elif ls[2] == 'gene' or 'ID' in info and info['ID'].startswith('gene'):
                info['strand'] = ls[6]
                info['chr'] = chrom
                _set_alias(info, {'ID': ['gene_id']})
                _set_alias(info, {'name': ['Name', 'gene_name']}, required=False)
                ref_info = {k: v for k, v in info.items() if k not in Gene.required_infos + ['name']}
                info = {k: info[k] for k in Gene.required_infos + ['name'] if k in info}
                info['properties'] = ref_info
                genes.setdefault(chrom, {})[info['ID']] = (info, start, end)
            elif all([v in info for v in ['Parent', "ID"]]) and (ls[2] == 'transcript' or info['Parent'].startswith('gene')):  # those denote transcripts
                tr_info = {k: v for k, v in info.items() if k.startswith('transcript_')}
                transcripts.setdefault(info["Parent"], {})[info['ID']] = tr_info
            elif ls[2] == 'start_codon' and 'Parent' in info:
                cds_start[info['Parent']] = end if ls[6] == '-' else start
            elif ls[2] == 'stop_codon' and 'Parent' in info:
                cds_stop[info['Parent']] = start if ls[6] == '-' else end
            else:
                skipped.add(ls[2])  # transcript infos?
    return exons, transcripts, genes, cds_start, cds_stop, skipped


def import_ref_transcripts(fn, transcriptome, file_format, chromosomes=None, gene_categories=None, short_exon_th=25, **kwargs):
    '''import transcripts from gff/gtf file (e.g. for a reference)
    returns a dict interval trees for the genes'''
    if gene_categories is None:
        gene_categories = ['gene']
    if file_format == 'gtf':
        exons, transcripts, gene_infos, cds_start, cds_stop, skipped = _read_gtf_file(fn, chromosomes, **kwargs)
    else:  # gff/gff3
        exons, transcripts, gene_infos, cds_start, cds_stop, skipped = _read_gff_file(fn, chromosomes, **kwargs)

    if skipped:
        logger.info('skipped the following categories: %s', skipped)

    logger.debug('construct interval trees for genes...')
    genes = {}
    for chrom in gene_infos:
        for info, _, _ in gene_infos[chrom].values():
            try:
                info['reference'] = info.pop('properties')
            except KeyError:
                logger.error(info)
                raise
        genes[chrom] = IntervalTree(Gene(start, end, info, transcriptome) for info, start, end in gene_infos[chrom].values())

    # sort the exons
    logger.debug('sorting exon positions...')
    for tid in exons:
        exons[tid].sort()
    missed_genes = [gid for gid in transcripts.keys() if gid not in gene_infos]
    if missed_genes:
        # logger.debug('/n'.join(gid+str(tr) for gid, tr in missed_genes.items()))
        notfound = len(missed_genes)
        found = sum((len(t) for t in genes.values()))
        logger.warning('Missing genes! Found gene information in categories %s for %s/%s genes', gene_categories, found, found + notfound)
    logger.debug('building gene data structure...')
    # add transcripts to genes
    for chrom in genes:
        for gene in genes[chrom]:
            g_id = gene.id
            tr = transcripts.get(g_id, {g_id: {}})
            for t_id, tr_info in tr.items():
                tr_info['transcript_id'] = t_id
                try:
                    tr_info['exons'] = exons[t_id]
                except KeyError:
                    # genes without exons get a single exons transcript
                    tr_info['exons'] = [tuple(gene[:2])]
                # add cds
                if t_id in cds_start and t_id in cds_stop:
                    tr_info['CDS'] = (cds_start[t_id], cds_stop[t_id]) if cds_start[t_id] < cds_stop[t_id] else (cds_stop[t_id], cds_start[t_id])
                gene.data['reference'].setdefault('transcripts', []).append(tr_info)
            if short_exon_th is not None:
                short_exons = {e for tr in gene.data['reference']['transcripts'] for e in tr['exons'] if e[1] - e[0] <= short_exon_th}
                if short_exons:
                    gene.data['reference']['short_exons'] = short_exons
    return genes


def collapse_immune_genes(self, maxgap=300000):
    ''' This function collapses annotation of immune genes (IG and TR) of a loci.

    As immune genes are so variable, classical annotation as a set of transcripts is not meaningfull for those genes.
    In consequence, each component of an immune gene is usually stored as an individual gene.
    This can cause issues when comparing transcripts to these genes, which naturally would overlap many of these components.
    To avoid these issues, immunoglobulin and T-cell receptor genes of a locus are combined to a single gene,
    without specifiying transcripts.
    Immune genes are recognized by the gff/gtf property "gene_type" set to "IG*_gene" or "TR*_gene".
    Components within the distance of "maxgap" get collapsed to a single gene called TR/IG_locus_X.
    :param maxgap: Specify maximum distance between components of the same locus.
    '''
    assert not self.samples, 'immune gene collapsing has to be called before adding long read samples'
    num = {'IG': 0, 'TR': 0}
    for chrom in self.data:
        for strand in ('+', '-'):
            immune = {'IG': [], 'TR': []}
            for g in self.data[chrom]:
                if g.strand != strand or not g.is_annotated or 'gene_type' not in g.data['reference']:
                    continue
                gtype = g.data['reference']['gene_type']
                if gtype[:2] in immune and gtype[-5:] == '_gene':
                    immune[gtype[:2]].append(g)
            for itype in immune:
                immune[itype].sort(key=lambda x: (x.start, x.end))
                offset = 0
                for i, g in enumerate(immune[itype]):
                    self.data[chrom].remove(g)
                    if i + 1 == len(immune[itype]) or g.end - immune[itype][i + 1].start > maxgap:
                        ref_info = {'gene_type': f'{itype}_gene', 'transcripts': [t for g in immune[itype][offset:i + 1] for t in g.ref_transcripts]}
                        info = {'ID': f'{itype}_locus_{num[itype]}', 'strand': strand, 'chr': chrom, 'reference': ref_info}
                        start = immune[itype][offset].start
                        end = immune[itype][i].end
                        new_gene = Gene(start, end, info, self)
                        self.data[chrom].add(new_gene)
                        num[itype] += 1
                        offset = i + 1
    logger.info('collapsed %s immunoglobulin loci and %s T-cell receptor loci', num["IG"], num["TR"])


# io utility functions
@ experimental
def get_mutations_from_bam(bam_file, genome_file, region, min_cov=.05):
    '''not very efficient function to fetch mutations within a region from a bam file
    not exported so far'''
    mut = dict()
    exons = []
    n = 0
    with AlignmentFile(bam_file, "rb") as align:
        for read in align.fetch(*region):
            n += 1

            exons.append(junctions_from_cigar(read.cigartuples, read.reference_start))
            mutations = get_mutations(read.cigartuples, read.query_sequence, read.reference_start, read.query_qualities)
            for pos, ref, alt, qual in mutations:
                mut.setdefault(pos, {}).setdefault(alt, [0, ref, []])
                mut[pos][alt][0] += 1
                if qual:
                    mut[pos][alt][2].append(qual)
    if min_cov < 1:
        min_cov = n * min_cov

    mut = {pos: v for pos, v in mut.items() if sum(v[alt][0] for alt in v) > min_cov}
    with FastaFile(genome_file) as genome_fh:
        for pos, v in mut.items():
            for alt in v.values():
                alt[1] = '' if alt[1] < 0 else genome_fh.fetch(region[0], pos, pos + alt[1])
            for tr in exons:
                for e in tr:
                    if pos >= e[0] and pos <= e[1]:
                        mut[pos]['cov'] = mut[pos].get('cov', 0) + 1
    return mut


def get_mutations(cigartuples, seq, ref_start, qual):
    'look up the bases affected by mutations as reported in the cigar string'
    # cigar numbers:
    # 012345678
    # MIDNSHP=X
    mutations = []
    ref_pos = ref_start
    seq_pos = 0
    for cigar in cigartuples:
        if cigar[0] in (1, 2, 8):  # I(ins), D(del) or X (missmatch):
            ref = -cigar[1] if cigar[0] == 1 else cigar[1]
            alt_base = '' if cigar[0] == 2 else seq[seq_pos:(seq_pos + cigar[1])]
            mutations.append((ref_pos, ref, alt_base, qual[seq_pos] if qual else None))
        if cigar[0] in (0, 2, 3, 7, 8):  # MDN=X -> move forward on reference
            ref_pos += cigar[1]
        if cigar[0] in (0, 1, 4, 7, 8):  # MIS=X -> move forward on seq
            seq_pos += cigar[1]
    return mutations


def aligned_part(cigartuples, is_reverse):
    "returns the interval of the trasncript that is aligned (e.g. not clipped) according to cigar. Positions are according to transcript strand"
    start = end = 0
    for cigar in reversed(cigartuples) if is_reverse else cigartuples:
        if cigar[0] in (0, 1, 7, 8):  # MI=X -> move forward on read:
            end += cigar[1]
        elif cigar[0] in (4, 5):  # clipping at end
            if end > start:
                return (start, end)
            end += cigar[1]
            start = end
    return (start, end)  # clipping at begining or no clipping


def get_clipping(cigartuples, pos):
    if cigartuples[0][0] == 4:
        # clipping at the begining
        return (pos, -cigartuples[0][1])
    elif cigartuples[-1][0] == 4:
        # clipping at the end - get the reference position
        return (pos + sum(c[1] for c in cigartuples[:-1] if c[0] in (0, 2, 3, 7, 8)), cigartuples[-1][1])  # MDN=X -> move forward on reference:
    else:
        return None


def _set_alias(d, alias, required=True):
    for pref, alt in alias.items():
        alt = [a for a in alt if a in d]
        if pref not in d:
            try:
                d[pref] = next(d[a] for a in alt)
            except StopIteration:
                if not required:
                    continue
                logger.error('did not find alternative for %s- suggested terms are %s, but have only those keys: %s', pref, alt, list(d))
                raise
        for a in alt:
            d.pop(a, None)


# human readable output
def gene_table(self, **filter_args):  # ideas: extra_columns
    '''Creates a gene summary table.

    Exports all genes within region to a table.

    :param filter_args: Parameters (e.g. "region", "query") are passed to Transcriptome.iter_genes.'''

    colnames = ['chr', 'start', 'end', 'strand', 'gene_id', 'gene_name', 'n_transcripts']
    rows = [(g.chrom, g.start, g.end, g.strand, g.id, g.name, g.n_transcripts) for g in self.iter_genes(**filter_args)]
    df = pd.DataFrame(rows, columns=colnames)
    return df


def transcript_table(self,  samples=None,  groups=None, coverage=False, tpm=False, tpm_pseudocount=0, extra_columns=None,  **filter_args):
    '''Creates a transcript table.

    Exports all transcript isoforms within region to a table.

    :param samples: provide a list of samples for which coverage / expression information is added.
    :param groups: provide groups as a dict (as from Transcriptome.groups()), for which coverage  / expression information is added.
    :param coverage: If set, coverage information is added for specified samples / groups.
    :param tpm: If set, expression information (in tpm) is added for specified samples / groups.
    :param tpm_pseudocount: This value is added to the coverage for each transcript, before calculating tpm.
    :param extra_columns: Specify the additional information added to the table.
        These can be any transcrit property as defined by the key in the transcript dict.
    :param filter_args: Parameters (e.g. "region", "query", "min_coverage",...) are passed to Transcriptome.iter_transcripts.'''

    if samples is None:
        if groups is None:
            samples = self.samples
        else:
            samples = []
    if groups is None:
        groups = {}
    if coverage is False and tpm is False:
        samples = []
        groups = {}
    if extra_columns is None:
        extra_columns = []
    if samples is None:
        samples = self.samples
    samples_set = set(samples)
    samples_set.update(*groups.values())
    assert all(s in self.samples for s in samples_set), 'Not all specified samples are known'
    if len(samples_set) == len(self.samples):
        all_samples = True
        sample_i = slice(None)
    else:
        all_samples = False
        sample_i = [i for i, sa in enumerate(self.samples) if sa in samples_set]

    if not isinstance(extra_columns, list):
        raise ValueError('extra_columns should be provided as list')

    colnames = ['chr', 'transcript_start', 'transcript_end', 'strand', 'gene_id', 'gene_name', 'transcript_nr',
                'transcript_length', 'num_exons', 'exon_starts', 'exon_ends', 'novelty_class', 'novelty_subclasses']
    colnames += extra_columns

    rows = []
    cov = []
    for g, trids, trs in self.iter_transcripts(**filter_args, genewise=True):
        if sample_i:
            idx = (slice(None), trids) if all_samples else np.ix_(sample_i, trids)
            cov.append(g.coverage[idx])
        for trid, tr in zip(trids, trs):
            exons = tr['exons']
            trlen = sum(e[1]-e[0] for e in exons)
            nov_class, subcat = tr['annotation']
            # subcat_string = ';'.join(k if v is None else '{}:{}'.format(k, v) for k, v in subcat.items())
            e_starts, e_ends = (','.join(str(exons[i][j]) for i in range(len(exons))) for j in range(2))
            row = [g.chrom, exons[0][0], exons[-1][1], g.strand, g.id, g.name, trid, trlen, len(exons), e_starts, e_ends,
                   SPLICE_CATEGORY[nov_class], ','.join(subcat)]
            for k in extra_columns:
                val = tr.get(k, 'NA')
                row.append(str(val) if isinstance(val, Iterable) else val)
            rows.append(row)

    # add coverage information
    df = pd.DataFrame(rows, columns=colnames)
    if cov:
        df_list = [df]
        cov = pd.DataFrame(np.concatenate(cov, 1).T, columns=self.samples if all_samples else [sa for i, sa in enumerate(self.samples) if i in sample_i])
        stab = self.sample_table.set_index('name')
        if samples:
            if coverage:
                df_list.append(cov[samples].add_suffix('_coverage'))
            if tpm:
                total = stab.loc[samples, 'nonchimeric_reads']+tpm_pseudocount*cov.shape[0]
                df_list.append(((cov[samples]+tpm_pseudocount)/total*1e6).add_suffix('_tpm'))
        if groups:
            cov_gr = pd.DataFrame({gn: cov[sa].sum(1) for gn, sa in groups.items()})
            if coverage:
                df_list.append(cov_gr.add_suffix('_sum_coverage'))
            if tpm:
                total = {gn: stab.loc[sa, 'nonchimeric_reads'].sum()+tpm_pseudocount*cov.shape[0] for gn, sa in groups.items()}
                df_list.append(((cov_gr+tpm_pseudocount)/total*1e6).add_suffix('_sum_tpm'))
        df = pd.concat(df_list, axis=1)

    return df


@ experimental
def chimeric_table(self, region=None, query=None):  # , star_chimeric=None, illu_len=200):
    '''Creates a chimeric table

    This table contains relevant infos about breakpoints and coverage for chimeric genes.

    :param region: Specify the region, either as (chr, start, end) tuple or as "chr:start-end" string. If omitted specify the complete genome.
    :param query: Specify transcript filter query.
    '''
    # todo: correct handeling of three part fusion events not yet implemented
    # todo: ambiguous alignment handling not yet implemented

    # if star_chimeric is None:
    #    star_chimeric=dict()
    # assert isinstance(star_chimeric, dict)
    if region is not None or query is not None:
        raise NotImplementedError
    chim_tab = list()
    for bp, chimeric in self.chimeric.items():
        cov = tuple(sum(c.get(sa, 0) for c, _ in chimeric) for sa in self.samples)
        genes = [info[4] if info[4] is not None else 'intergenic' for info in chimeric[0][1]]
        for i, bp_i in enumerate(bp):
            chim_tab.append(('_'.join(genes),) + bp_i[: 3] + (genes[i],) + bp_i[3:] + (genes[i + 1],) + (sum(cov),) + cov)
    chim_tab = pd.DataFrame(chim_tab, columns=['name', 'chr1', 'strand1', 'breakpoint1', 'gene1', 'chr2', 'strand2',
                            'breakpoint2', 'gene2', 'total_cov'] + [s + '_cov' for s in self.infos['sample_table'].name])

    return chim_tab

    # todo: integrate short read coverage from star files
#   breakpoints = {}  # todo: this should be the isoseq breakpoints
#   offset = 10 + len(self.infos['sample_table'])
#   for sa_idx, sa in enumerate(star_chimeric):
#       star_tab = pd.read_csv(star_chimeric[sa], sep='\t')
#       for _, row in star_tab.iterrows():
#           if row['chr_donorA'] in breakpoints and row['chr_acceptorB'] in breakpoints:
#               idx1 = {bp.data for bp in breakpoints[row['chr_donorA']][row['brkpt_donorA']]}
#               if idx1:
#                   idx2 = {bp.data for bp in breakpoints[row['chr_acceptorB']][row['brkpt_acceptorB']]}
#                   idx_ol = {idx for idx, snd in idx2 if (idx, not snd) in idx1}
#                   for idx in idx_ol:
#                       chim_tab[idx][offset + sa_idx] += 1
#
#    chim_tab = pd.DataFrame(chim_tab, columns=['trid', 'len', 'gene1', 'part1', 'breakpoint1', 'gene2', 'part2', 'breakpoint2',
#                            'total_cov'] + [s + '_cov' for s in self.infos['sample_table'].name] + [s + "_shortread_cov" for s in star_chimeric])
#    return chim_tab


def write_gtf(self, fn, source='isotools', gzip=False, **filter_args):
    '''Exports the transcripts in gtf format to a file.

    :param fn: The filename to write the gtf.
    :param source: String for the source column of the gtf file.
    :param region: Splecify genomic region to export to gtf. If omitted, export whole genome.
    :param query: Specify transcript filter query.
    :param gzip: compress the output as gzip.'''

    def openfile(fn):
        if gzip:
            return gziplib.open(fn, 'wt')
        else:
            return open(fn, 'w', encoding="utf8")

    with openfile(fn) as f:
        logger.info('writing %sgtf file to %s', "gzip compressed " if gzip else "", fn)
        for g, trids, _ in self.iter_transcripts(genewise=True, **filter_args):
            lines = g._to_gtf(trids=trids, source=source)
            _ = f.write('\n'.join(('\t'.join(str(field) for field in line) for line in lines)) + '\n')


def export_alternative_splicing(self, out_dir, out_format='mats', reference=False, min_total=100,
                                min_alt_fraction=.1, samples=None, region=None, query=None, progress_bar=True):
    '''Exports alternative splicing events defined by the transcriptome.

    This is intended to integrate splicing event analysis from short read data.
    Tools for short read data implement different formats for the import of events.
    These formats include several files and depend on specific file naming.
    Currently only MISO (out_format="miso") and rMATS (out_format='mats') are supported.
    rMATS is recommended.

    :param out_dir: Path to the directory where the event files are written to.
    :param out_format: Specify the output format. Must be either "miso" or "mats".
    :param min_total: Minimum total coverage over all selected samples.
    :param region: Specify the region, either as (chr, start, end) tuple or as "chr:start-end" string.
        If omitted specify the complete genome.
    :param query: Specify gene filter query.
    :param progress_bar: Show the progress.
    :param reference: If set to True, the LRTS data is ignored and the events are called from the reference.
        In this case the following parameters are ignored
    :param samples: Specify the samples to consider
    :param min_total: Minimum total coverage over all selected samples.
    :param min_alt_fraction: Minimum fraction of reads supporting the alternative.'''
    if out_format == 'miso':
        fn = 'isotools_miso_{}.gff'
        alt_splice_export = _miso_alt_splice_export
    elif out_format == 'mats':
        fn = 'fromGTF.{}.txt'
        alt_splice_export = _mats_alt_splice_export
    else:
        raise ValueError('out_format must be "miso" or "mats"')

    types = {'ES': 'SE', '3AS': 'A3SS', '5AS': 'A5SS', 'IR': 'RI', 'ME': 'MXE'}  # it looks like these are the "official" identifiers?
    out_file = {st: out_dir + '/' + fn.format(st) for st in types.values()}
    if samples is None:
        samples = self.samples
    assert all(s in self.samples for s in samples), 'not all specified samples found'
    sa_dict = {sa: i for i, sa in enumerate(self.samples)}
    sidx = np.array([sa_dict[sa] for sa in samples])

    assert 0 < min_alt_fraction < .5, 'min_alt_fraction must be > 0 and < 0.5'
    count = {st: 0 for st in types.values()}
    with ExitStack() as stack:
        fh = {st: stack.enter_context(open(out_file[st], 'w')) for st in out_file}
        if out_format == 'mats':  # prepare mats header
            base_header = ['ID', 'GeneID', 'geneSymbol', 'chr', 'strand']
            add_header = {'SE': ['exonStart_0base', 'exonEnd', 'upstreamES', 'upstreamEE', 'downstreamES', 'downstreamEE'],
                          'RI': ['riExonStart_0base', 'riExonEnd', 'upstreamES', 'upstreamEE', 'downstreamES', 'downstreamEE'],
                          'MXE': ['1stExonStart_0base', '1stExonEnd', '2ndExonStart_0base', '2ndExonEnd', 'upstreamES',
                                  'upstreamEE', 'downstreamES', 'downstreamEE'],
                          'A3SS': ['longExonStart_0base', 'longExonEnd', 'shortES', 'shortEE', 'flankingES', 'flankingEE'],
                          'A5SS': ['longExonStart_0base', 'longExonEnd', 'shortES', 'shortEE', 'flankingES', 'flankingEE']}
            for st in fh:
                fh[st].write('\t'.join(base_header + add_header[st]) + '\n')
        for g in self.iter_genes(region, query, progress_bar=progress_bar):
            if reference and not g.is_annotated:
                continue
            elif not reference and g.coverage[sidx, :].sum() < min_total:
                continue

            seg_graph = g.ref_segment_graph if reference else g.segment_graph
            for setA, setB, nodeX, nodeY, splice_type in seg_graph.find_splice_bubbles(types=('ES', '3AS', '5AS', 'IR', 'ME')):
                if not reference:
                    junction_cov = g.coverage[np.ix_(sidx, setA)].sum(1)
                    total_cov = g.coverage[np.ix_(sidx, setB)].sum(1) + junction_cov
                    if total_cov.sum() < min_total or (not min_alt_fraction < junction_cov.sum() / total_cov.sum() < 1 - min_alt_fraction):
                        continue
                st = types[splice_type]
                lines = alt_splice_export(setA, setB, nodeX, nodeY, st, reference, g, count[st])
                if lines:
                    count[st] += len(lines)
                    fh[st].write('\n'.join(('\t'.join(str(field) for field in line) for line in lines)) + '\n')


def _miso_alt_splice_export(setA, setB, nodeX, nodeY, st, reference, g, offset):
    seg_graph = g.ref_segment_graph if reference else g.segment_graph

    event_id = f'{g.chrom}:{seg_graph[nodeX].end}-{seg_graph[nodeY].start}_st'
    # TODO: Mutually exclusives extend beyond nodeY - and have potentially multiple A "mRNAs"
    # TODO: is it possible to extend exons at nodeX and Y - if all/"most" tr from setA and B agree?
    # if st=='ME':
    #    nodeY=min(seg_graph._pas[setA])
    lines = []
    lines.append([g.chrom, st, 'gene', seg_graph[nodeX].start, seg_graph[nodeY].end, '.', g.strand, '.', f'ID={event_id};gene_name={g.name};gene_id={g.id}'])
    # lines.append((g.chrom, st, 'mRNA', seg_graph[nodeX].start, seg_graph[nodeY].end, '.',g.strand, '.', f'Parent={event_id};ID={event_id}.A'))
    # lines.append((g.chrom, st, 'exon', seg_graph[nodeX].start, seg_graph[nodeX].end, '.',g.strand, '.', f'Parent={event_id}.A;ID={event_id}.A.up'))
    # lines.append((g.chrom, st, 'exon', seg_graph[nodeY].start, seg_graph[nodeY].end, '.',g.strand, '.', f'Parent={event_id}.A;ID={event_id}.A.down'))
    for i, exons in enumerate({tuple(seg_graph._get_all_exons(nodeX, nodeY, tr)) for tr in setA}):
        lines.append((g.chrom, st, 'mRNA', exons[0][0], exons[-1][1], '.', g.strand, '.', f'Parent={event_id};ID={event_id}.A{i}'))
        lines[0][3] = min(lines[0][3], lines[-1][3])
        lines[0][4] = max(lines[0][4], lines[-1][4])
        for j, e in enumerate(exons):
            lines.append((g.chrom, st, 'exon', e[0], e[1], '.', g.strand, '.', f'Parent={event_id}.A{i};ID={event_id}.A{i}.{j}'))
    for i, exons in enumerate({tuple(seg_graph._get_all_exons(nodeX, nodeY, tr)) for tr in setB}):
        lines.append((g.chrom, st, 'mRNA', exons[0][0], exons[-1][1], '.', g.strand, '.', f'Parent={event_id};ID={event_id}.B{i}'))
        lines[0][3] = min(lines[0][3], lines[-1][3])
        lines[0][4] = max(lines[0][4], lines[-1][4])
        for j, e in enumerate(exons):
            lines.append((g.chrom, st, 'exon', e[0], e[1], '.', g.strand, '.', f'Parent={event_id}.B{i};ID={event_id}.B{i}.{j}'))
    return lines


def _mats_alt_splice_export(setA, setB, nodeX, nodeY, st, reference, g, offset,  use_top_isoform=True, use_top_alternative=True):
    # use_top_isoform and use_top_alternative are ment to simplify the output, in order to not confuse rMATS with to many options
    # 'ID','GeneID','geneSymbol','chr','strand'
    # and ES/EE for the relevant exons
    # in case of 'SE':['skipped', 'upstream', 'downstream'],
    # in case of 'RI':['retained', 'upstream', 'downstream'],
    # in case of 'MXE':['1st','2nd', 'upstream', 'downstream'],
    # in case of 'A3SS':['long','short', 'flanking'],
    # in case of 'A5SS':['long','short', 'flanking']}
    # upstream and downstream/ 1st/snd are with respect to the genome strand
    # offset is the event id offset
    seg_graph = g.ref_segment_graph if reference else g.segment_graph

    lines = []
    if g.chrom[: 3] != 'chr':
        chrom = 'chr' + g.chrom
    else:
        chrom = g.chrom
    if use_top_isoform:  # use flanking exons from top isoform
        all_transcript_ids = setA+setB
        if not reference:
            # most covered isoform
            top_isoform = all_transcript_ids[g.coverage[:, all_transcript_ids].sum(0).argmax()]  # top covered isoform across all samples
            nodeX_start = seg_graph._get_exon_start(top_isoform, nodeX)
            nodeY_end = seg_graph._get_exon_end(top_isoform, nodeY)
        else:
            # for reference: most frequent
            nodeX_start = Counter([seg_graph._get_exon_start(n, nodeX) for n in all_transcript_ids]).most_common(1)[0][0]
            nodeY_end = Counter([seg_graph._get_exon_end(n, nodeY) for n in all_transcript_ids]).most_common(1)[0][0]

        exonsA = ((seg_graph[nodeX_start].start, seg_graph[nodeX].end), (seg_graph[nodeY].start, seg_graph[nodeY_end].end))  # flanking/outer "exons" of setA()
    else:
        exonsA = ((seg_graph[nodeX].start, seg_graph[nodeX].end), (seg_graph[nodeY].start, seg_graph[nodeY].end))  # flanking/outer "exons" of setA

    # _get_all_exons does not extend the exons beyond the nodeX/Y
    alternatives = [tuple(seg_graph._get_all_exons(nodeX, nodeY, b_tr)) for b_tr in setB]
    if use_top_alternative:
        if reference:
            c = Counter(alternatives)
        else:
            weights = [g.coverage[:, b_tr].sum() for b_tr in setB]
            c = Counter()
            for alt, w in zip(alternatives, weights):
                c.update({alt: w})
        alternatives = [c.most_common(1)[0][0]]
    else:
        alternatives = set(alternatives)
    for exonsB in alternatives:
        exons_sel = []
        if st in ['A3SS', 'A5SS'] and len(exonsB) == 2:
            if exonsA[0][1] == exonsB[0][1]:  # A5SS on - strand or A3SS on + strand
                exons_sel.append([(exonsB[1][0], exonsA[1][1]), exonsA[1], exonsA[0]])  # long short flanking
            else:  # A5SS on + strand or A3SS on - strand
                exons_sel.append([(exonsA[0][0], exonsB[0][1]), exonsA[0], exonsA[1]])  # long short flanking
        elif st == 'SE' and len(exonsB) == 3:
            # just to be sure everything is consistent
            assert exonsA[0][1] == exonsB[0][1] and exonsA[1][0] == exonsB[2][0], f'invalid exon skipping {exonsA} vs {exonsB}'
            # e_order = (1, 0, 2) if g.strand == '+' else (1, 2, 0)
            exons_sel.append([exonsB[i] for i in (1, 0, 2)])  # skipped, upstream, downstream
        elif st == 'RI' and len(exonsB) == 1:
            exons_sel.append([(exonsA[0][0], exonsA[1][1]), exonsA[0], exonsA[1]])  # retained, upstream, downstream
            # if g.strand == '+' else [exonsB[0], exonsA[1], exonsA[0]])
        elif st == 'MXE' and len(exonsB) == 3:
            # nodeZ=next(idx for idx,n in enumerate(seg_graph) if n.start==exonsB[-1][0])
            # multiple exonA possibilities, so we need to check all of them
            for exonsA_ME in {tuple(seg_graph._get_all_exons(nodeX, nodeY, a_tr)) for a_tr in setA}:
                if len(exonsA_ME) != 3:  # complex events are not possible in rMATS
                    continue
                assert exonsA_ME[0] == exonsB[0] and exonsA_ME[2] == exonsB[2]  # should always be true
                # assert exonsA_ME[0][1] == exonsA[0][1] and exonsA_ME[2][0] == exonsA[1][0]  # should always be true
                # '1st','2nd', 'upstream', 'downstream'
                exons_sel.append([exonsB[1], exonsA_ME[1], exonsA[0], exonsA[1]])
        for exons in exons_sel:  # usually there is only one rMATS event per exonB, but for MXE we may get several
            # lines.append([f'"{g.id}"', f'"{g.name}"', chrom, g.strand] + [pos for e in exons for pos in ((e[1],e[0]) if g.strand == '-' else e)])
            lines.append([f'"{g.id}"', f'"{g.name}"', chrom, g.strand] + [pos for e in exons for pos in e])  # no need to reverse the order of exon start/end
    return [[offset + count] + l for count, l in enumerate(lines)]


def get_gff_chrom_dict(gff, chromosomes):
    'fetch chromosome ids - in case they use ids in gff for the chormosomes'
    chrom = {}
    for c in gff.contigs:
        # loggin.debug ("---"+c)
        for line in gff.fetch(c, 1, 2):  # chromosomes span the entire chromosome, so they can be fetched like that
            if line[1] == "C":
                ls = line.split(sep="\t")
                if ls[2] == "region":
                    info = dict([pair.split("=")
                                 for pair in ls[8].split(";")])
                    if "chromosome" in info.keys():
                        if chromosomes is None or info["chromosome"] in chromosomes:
                            chrom[ls[0]] = info["chromosome"]
                        break

        else:  # no specific regions entries - no aliases
            if chromosomes is None or c in chromosomes:
                chrom[c] = c
    gff.seek(0)
    return chrom


class IntervalArray:
    '''drop in replacement for the interval tree during construction, with faster lookup'''

    def __init__(self, total_size, bin_size=1e4):
        self.obj = {}
        self.data = [set() for _ in range(int((total_size) // bin_size) + 1)]
        self.bin_size = bin_size

    def overlap(self, begin, end):
        try:
            candidates = {obj_id for idx in range(int(begin // self.bin_size), int(end // self.bin_size) + 1) for obj_id in self.data[idx]}
        except IndexError:
            logger.error('requesting interval between %s and %s, but array is allocated only until position %s', begin, end, len(self.data)*self.bin_size)
            raise
        return (self.obj[obj_id] for obj_id in candidates if has_overlap((begin, end), self.obj[obj_id]))  # this assumes object has range obj[0] to obj[1]

    def add(self, obj):
        self.obj[id(obj)] = obj
        try:
            for idx in range(int(obj.begin // self.bin_size), int(obj.end // self.bin_size) + 1):
                self.data[idx].add(id(obj))
        except IndexError:
            logger.error('adding interval from %s to %s, but array is allocated only until position %s', obj.begin, obj.end, len(self.data)*self.bin_size)
            raise

    def __len__(self):
        return len(self.obj)

    def __iter__(self):
        return (v for v in self.obj.values())
