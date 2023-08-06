from pysam import FastaFile
from tqdm import tqdm
import logging
import re
from ._utils import _filter_function

logger = logging.getLogger('isotools')
BOOL_OP = {'and', 'or', 'not', 'is'}
DEFAULT_GENE_FILTER = {'NOVEL_GENE': 'not reference',
                       'EXPRESSED': 'transcripts',
                       'CHIMERIC': 'chimeric'}

DEFAULT_REF_TRANSCRIPT_FILTER = {
    'REF_UNSPLICED': 'len(exons)==1',
    'REF_MULTIEXON': 'len(exons)>1',
    'REF_INTERNAL_PRIMING': 'downstream_A_content>.5'}

DEFAULT_TRANSCRIPT_FILTER = {
    # 'CLIPPED_ALIGNMENT':'clipping',
    'INTERNAL_PRIMING': 'len(exons)==1 and downstream_A_content and downstream_A_content>.5',  # more than 50% a
    'RTTS': 'noncanonical_splicing is not None and novel_splice_sites is not None and \
        any(2*i in novel_splice_sites and 2*i+1 in novel_splice_sites for i,_ in noncanonical_splicing)',
    'NONCANONICAL_SPLICING': 'noncanonical_splicing',
    'NOVEL_TRANSCRIPT': 'annotation[0]>0',
    'FRAGMENT': 'fragments and any("novel exonic " in a or "fragment" in a for a in annotation[1])',
    'UNSPLICED': 'len(exons)==1',
    'MULTIEXON': 'len(exons)>1',
    'SUBSTANTIAL': 'g.coverage.sum() * .01 < g.coverage[:,trid].sum()'
}

SPLICE_CATEGORY = ['FSM', 'ISM', 'NIC', 'NNC', 'NOVEL']


ANNOTATION_VOCABULARY = ['antisense', 'intergenic', 'genic genomic', 'novel exonic PAS', 'novel intronic PAS', 'readthrough fusion',
                         'novel exon', "novel 3' splice site", 'intron retention', "novel 5' splice site", 'exon skipping', 'novel combination',
                         'novel intronic TSS', 'novel exonic TSS', 'mono-exon', 'novel junction', "5' fragment", "3' fragment", 'intronic']


# filtering functions for the transcriptome class

def add_orf_prediction(self, genome_fn, progress_bar=True, fickett_score=True, hexamer_file=None):
    ''' Performs ORF prediction on the transcripts.

    For each transcript the longest open reading frame is determined, and metrics to assess the coding potential
    (UTR and CDS lenghts, Fickett score, hexamer score and NMD prediction). The hexamer score depends on hexamer frequency table,
    see CPAT python module for prebuild tables and instructions.

    :param geneome_fn: Path to the genome in fastA format.
    :param fickett_score: If set to True, the Fickett TESTCODE score is computed for each transcript.
    :param hexamer_file: Filename of the hexamer table, for the ORF hexamer scores. If set not None, the hexamer score is not computed.'''

    if hexamer_file is None:
        coding = None
        noncoding = None
    else:
        coding = {}
        noncoding = {}
        for line in open(hexamer_file):
            line = line.strip()
            fields = line.split()
            if fields[0] == 'hexamer':
                continue
            coding[fields[0]] = float(fields[1])
            noncoding[fields[0]] = float(fields[2])

    with FastaFile(genome_fn) as genome_fh:
        missing_chr = set(self.chromosomes) - set(genome_fh.references)
        if missing_chr:
            missing_genes = sum(len(self.data[mc]) for mc in missing_chr)
            logger.warning('%s contigs are not contained in genome, affecting %s genes. \
                ORFs cannot be computed for these contigs: %s', str(len(missing_chr)), str(missing_genes), str(missing_chr))

        for g in self.iter_genes(progress_bar=progress_bar):
            if g.chrom in genome_fh.references:
                g.add_orfs(genome_fh, reference=False, minlen=30, get_fickett=fickett_score, coding_hexamers=coding, noncoding_hexamers=noncoding)
                g.add_orfs(genome_fh, reference=True, minlen=30, get_fickett=fickett_score, coding_hexamers=coding, noncoding_hexamers=noncoding)


def add_qc_metrics(self, genome_fn, progress_bar=True, downstream_a_len=30, direct_repeat_wd=15, direct_repeat_wobble=2, direct_repeat_mm=2,
                   unify_ends=True):
    ''' Retrieves QC metrics for the transcripts.

    Calling this function populates transcript["biases"] information, which can be used do create filters.
    In particular, the direct repeat length, the downstream adenosine content and information about non-canonical splice sites are fetched.
    In addition, genes are scanned for transcripts that are fully contained in other transcripts.

    :param geneome_fn: Path to the genome in fastA format.
    :param downstream_a_len: The number of bases downstream the transcript where the adenosine fraction is determined.
    :param direct_repeat_wd: The number of bases around the splice sites scanned for direct repeats.
    :param direct_repeat_wobble: Number of bases the splice site sequences are shifted.
    :param unify_ends: Unify TSS/PAS across transcripts of a gene.
    :param direct_repeat_mm: Maximum number of missmatches in a direct repeat.'''

    with FastaFile(genome_fn) as genome_fh:
        missing_chr = set(self.chromosomes) - set(genome_fh.references)
        if missing_chr:
            missing_genes = sum(len(self.data[mc]) for mc in missing_chr)
            logger.warning('%s contigs are not contained in genome, affecting %s genes. \
                Some metrics cannot be computed: %s', str(len(missing_chr)), str(missing_genes), str(missing_chr))

        for g in self.iter_genes(progress_bar=progress_bar):
            if unify_ends:
                # remove segmet graph (if unify TSS/PAS option selected)
                g.data['segment_graph'] = None
                # "unify" TSS/PAS (if unify TSS/PAS option selected)
                g._unify_ends()
            # compute segment graph (if not present)
            _ = g.segment_graph
            g.add_fragments()
            if g.chrom in genome_fh.references:
                g.add_direct_repeat_len(genome_fh, delta=direct_repeat_wd, max_mm=direct_repeat_mm, wobble=direct_repeat_wobble)
                g.add_noncanonical_splicing(genome_fh)
                g.add_threeprime_a_content(genome_fh, length=downstream_a_len)

    self.infos['biases'] = True  # flag to check that the function was called


def remove_filter(self, tag):
    '''Removes definition of filter tag.

    :param tag: Specify the tag of the filter definition to remove.'''
    old = [f.pop(tag, None) for f in self.filter.values()]
    if not any(old):
        logger.error('filter tag %s not found', tag)


def add_filter(self, tag, expression, context='transcript', update=False):
    '''Defines a new filter for gene, transcripts and reference transcripts.

    The provided expressions is evaluated during filtering in the provided context, when specified in a query string of a function that supports filtering.
    Importantly, filtering does not modify the original data; rather, it is only applied when specifying the query string.
    For examples, see the default filter definitions isotools.DEFAULT_GENE_FILTER,
    isotools.DEFAULT_TRANSCRIPT_FILTER and isotools.DEFAULT_REF_TRANSCRIPT_FILTER.

    :param tag: Unique tag identifer for this filter. Must be a single word.
    :param expression: Expression to be evaluated on gene, transcript, or reference transcript.
    :param context: The context for the filter expression, either "gene", "transcript" or "reference".
    :param update: If set, the already present definition of the provided tag gets overwritten.'''

    assert context in ['gene', 'transcript', 'reference'], "filter context must be 'gene', 'transcript' or 'reference'"
    assert tag == re.findall(r'\b\w+\b', tag)[0], '"tag" must be a single word'
    if not update:
        assert tag not in [f for f in self.filter.values()], "Filter tag is already present. Set update=True to re-define."
    if context == 'gene':
        attributes = {k for g in self for k in g.data.keys() if k.isidentifier()}
    else:
        attributes = {'g', 'trid'}
        if context == 'transcript':
            attributes.update({k for g in self for tr in g.transcripts for k in tr.keys() if k.isidentifier()})
        elif context == 'reference':
            attributes.update({k for g in self if g.is_annotated for tr in g.ref_transcripts for k in tr.keys() if k.isidentifier()})
    # used=re.findall(r'\b\w+\b', expression)

    try:  # test whether the expression can be evaluated
        _, f_args = _filter_function(expression)
        # _=f() # this would fail for many default expressions - can be avoided by checking if used attributes are None - but not ideal
        # Could be extended by dummy gene/transcript argument
    except BaseException:
        logger.error('expression cannot be evaluated:\n%s', expression)
        raise
    unknown_attr = [attr for attr in f_args if attr not in attributes]
    if unknown_attr:
        logger.warning("Some attributes not present in %s context, please make sure there is no typo: %s", context, ','.join(unknown_attr))
    if update:  # avoid the same tag in different context
        for old_context, filter_dict in self.filter.items():
            if filter_dict.pop(tag, None) is not None:
                logger.info('replaced existing filter rule %s in %s context', tag, old_context)
    self.filter[context][tag] = expression


def iter_genes(self, region=None, query=None, min_coverage=None, max_coverage=None, gois=None, progress_bar=False):
    '''Iterates over the genes of a region, optionally applying filters.

    :param region: The region to be considered. Either a string "chr:start-end", or a tuple (chr,start,end). Start and end is optional.
    :param query: If provided, query string is evaluated on all genes for filtering'''

    if query:
        query_fun, used_tags = _filter_function(query)
        # used_tags={tag for tag in re.findall(r'\b\w+\b', query) if tag not in BOOL_OP}
        all_filter = list(self.filter['gene'])
        msg = 'did not find the following filter rules: {}\nvalid rules are: {}'
        assert all(f in all_filter for f in used_tags), msg.format(
            ', '.join(f for f in used_tags if f not in all_filter), ', '.join(all_filter))
        filter_fun = {tag: _filter_function(self.filter['gene'][tag])[0] for tag in used_tags}

        try:  # test the filter expression with dummy tags
            query_fun(**{tag: True for tag in used_tags})
        except BaseException:
            logger.error("Error in query string: \n{query}")
            raise
    if region is None:
        if gois is None:
            genes = self
        else:
            genes = {self[goi] for goi in gois}

    else:
        if isinstance(region, str):
            if region in self.data:
                genes = self.data[region]  # provide chromosome
            else:  # parse region string (chr:start-end)
                try:
                    chrom, pos = region.split(':')
                    start, end = [int(i) for i in pos.split('-')]
                except BaseException as e:
                    raise ValueError('incorrect region {} - specify as string "chr" or "chr:start-end" or tuple ("chr",start,end)'.format(region)) from e
        elif isinstance(region, tuple):
            chrom, start, end = region
        if chrom in self.data:
            genes = self.data[chrom][int(start):int(end)]
        else:
            raise ValueError('specified chromosome {} not found'.format(chrom))
        if gois is not None:
            genes = [g for g in genes if g.id in gois or g.name in gois]

    for g in tqdm(genes, disable=not progress_bar, unit='genes', smoothing=0):  # often some genes take much longer than others - smoothing 0 means avg
        if min_coverage is not None and g.coverage.sum() < min_coverage:
            continue
        if max_coverage is not None and g.coverage.sum() > max_coverage:
            continue
        if query is None or query_fun(**{tag: fun(**g.data) for tag, fun in filter_fun.items()}):
            yield g


def iter_transcripts(self, region=None, query=None, min_coverage=None, max_coverage=None, genewise=False, gois=None, progress_bar=False):
    '''Iterates over the transcripts of a region, optionally applying filters.

    By default, each iteration returns a 3 Tuple with the gene object, the transcript number and the transcript dictionary.

    :param region: The region to be considered. Either a string "chr:start-end", or a tuple (chr,start,end). Start and end is optional.
    :param query: If provided, query string is evaluated on all transcripts for filtering
    :param min_coverage: The minimum coverage threshold. Transcripts with less reads in total are ignored.
    :param max_coverage: The maximum coverage threshold. Transcripts with more reads in total are ignored.
    :param genewise: In each iteration, return the gene and all transcript numbers and transcript dicts for the gene as tuples.
    :param gois: If provided, only transcripts from the list of genes of interest are considered. Provide as a list of gene ids or gene names.
        By default, all genes are considered
    :param progress_bar: Print a progress bar. '''

    if query:
        # used_tags={tag for tag in re.findall(r'\b\w+\b', query) if tag not in BOOL_OP}
        all_filter = list(self.filter['transcript']) + list(self.filter['gene'])
        query_fun, used_tags = _filter_function(query)
        msg = 'did not find the following filter rules: {}\nvalid rules are: {}'
        assert all(f in all_filter for f in used_tags), msg.format(
            ', '.join(f for f in used_tags if f not in all_filter), ', '.join(all_filter))
        tr_filter_fun = {tag: _filter_function(self.filter['transcript'][tag])[0] for tag in used_tags if tag in self.filter['transcript']}
        g_filter_fun = {tag: _filter_function(self.filter['gene'][tag])[0] for tag in used_tags if tag in self.filter['gene']}

        try:  # test the filter expression with dummy tags
            _ = query_fun(**{tag: True for tag in used_tags})
        except BaseException:
            logger.error("Error in query string: \n%s", query)
            raise
    else:
        tr_filter_fun = query_fun = None
        g_filter_fun = {}
    if genewise:
        for g in self.iter_genes(region=region, gois=gois, progress_bar=progress_bar):
            g_filter_eval = {tag: fun(**g.data) for tag, fun in g_filter_fun.items()}
            filter_result = tuple(_filter_transcripts(g, g.transcripts, query_fun, tr_filter_fun, g_filter_eval, min_coverage, max_coverage))
            if filter_result:
                i_tuple, tr_tuple = zip(*filter_result)
                yield g, i_tuple, tr_tuple
    else:
        for g in self.iter_genes(region=region, gois=gois, progress_bar=progress_bar):
            g_filter_eval = {tag: fun(**g.data) for tag, fun in g_filter_fun.items()}
            for i, tr in _filter_transcripts(g, g.transcripts, query_fun, tr_filter_fun, g_filter_eval, min_coverage, max_coverage):
                yield g, i, tr


def iter_ref_transcripts(self, region=None, query=None, genewise=False, gois=None, progress_bar=False):
    '''Iterates over the referemce transcripts of a region, optionally applying filters.

    :param region: The region to be considered. Either a string "chr:start-end", or a tuple (chr,start,end). Start and end is optional.
    :param genewise: In each iteration, return the gene and all transcript numbers and transcript dicts for the gene as tuples.
    :param query: If provided, query string is evaluated on all transcripts for filtering
    :param genewise: In each iteration, return the gene and all transcript numbers and transcript dicts for the gene as tuples.
    :param gois: If provided, only transcripts from the list of genes of interest are considered. Provide as a list of gene ids or gene names.
        By default, all genes are considered
    :param progress_bar: Print a progress bar. '''

    if query:
        # used_tags={tag for tag in re.findall(r'\b\w+\b', query) if tag not in BOOL_OP}
        all_filter = list(self.filter['reference']) + list(self.filter['gene'])
        query_fun, used_tags = _filter_function(query)
        msg = 'did not find the following filter rules: {}\nvalid rules are: {}'
        ref_filter_fun = {tag: _filter_function(self.filter['reference'][tag])[0] for tag in used_tags if tag in self.filter['reference']}
        g_filter_fun = {tag: _filter_function(self.filter['gene'][tag])[0] for tag in used_tags if tag in self.filter['gene']}
        assert all(f in all_filter for f in used_tags), msg.format(
            ', '.join(f for f in used_tags if f not in all_filter), ', '.join(all_filter))
        try:  # test the filter expression with dummy tags
            _ = query_fun(**{tag: True for tag in used_tags})
        except BaseException:
            logger.error("Error in query string: \n{query}")
            raise
    else:
        ref_filter_fun = query_fun = None
        g_filter_fun = {}
    if genewise:
        for g in self.iter_genes(region=region, gois=gois, progress_bar=progress_bar):
            g_filter_eval = {tag: fun(**g.data) for tag, fun in g_filter_fun.items()}
            filter_result = tuple(_filter_transcripts(g, g.ref_transcripts, query_fun, ref_filter_fun, g_filter_eval))
            if filter_result:
                i_tuple, tr_tuple = zip(*filter_result)
                yield g, i_tuple, tr_tuple
    else:
        for g in self.iter_genes(region=region, gois=gois, progress_bar=progress_bar):
            if g.is_annotated:
                g_filter_eval = {tag: fun(**g.data) for tag, fun in g_filter_fun.items()}
                for i, tr in _filter_transcripts(g, g.ref_transcripts, query_fun, ref_filter_fun, g_filter_eval):
                    yield g, i, tr


def _eval_filter_fun(fun, name, **args):
    '''Decorator for the filter functions, which are lambdas and thus cannot have normal decorators.
    On exceptions the provided parameters are reported. This is helpfull for debugging.'''
    try:
        return fun(**args)
    except Exception as e:
        logger.error('error when evaluating filter %s with arguments %s: %s', name, str(args), str(e))
        raise  # either stop evaluation
        # return False   #or continue


def _filter_transcripts(g, transcripts,  query_fun, filter_fun, g_filter_eval, mincoverage=None, maxcoverage=None):
    ''' Iterator over the transcripts of the gene.

    Transcrips are specified by lists of flags submitted to the parameters.

    :param query_fun: function to be evaluated on tags
    :param filter_fun: tags to be evalutated on transcripts'''
    for i, tr in enumerate(transcripts):
        if mincoverage and g.coverage[:, i].sum() < mincoverage:
            continue
        if maxcoverage and g.coverage[:, i].sum() > maxcoverage:
            continue
        query_result = query_fun is None or query_fun(
            **g_filter_eval, **{tag: _eval_filter_fun(f, tag, g=g, trid=i, **tr) for tag, f in filter_fun.items()})
        if query_result:
            yield i, tr
