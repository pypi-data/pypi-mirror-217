# marker alignments
This a Python package to process and summarise alignments of metagenomic sequencing reads to a reference database of marker genes. You can use it in conjunction with an aligner like `bowtie2` to produce an estimate of taxa present in a metagenomic sample.

Features:
- filtering reads on alignment properties
- summarizing by marker and taxon
- clustering based on multiple alignments per query
- quantification


## Usage

### Installation

Install via pip:
```
pip install marker_alignments
```

### Getting started

Download a small example alignment file, and run `marker_alignments` with most basic options:

```
wget "https://raw.githubusercontent.com/wbazant/marker_alignments/main/tests/data/example.sam"

marker_alignments --input example.sam --output /dev/stdout
```

If the package installed correctly, you should see a coverage report for each reference in the alignments file. Try it with your input file next, and take it from there: `marker_alignments --help` will show you all options about filtering and output types.

### Is this suitable for my data?

This package is for analysing metagenomic reads from whole genome sequencing, aligned to a reference of your choice.

An allowed input is an alignment file in `.sam` or `.bam` format, coming from `bowtie2` or similar enough: @SQ lines on top, reads and MD tags in the output. See [example .sam](https://raw.githubusercontent.com/wbazant/marker_alignments/main/tests/data/example.sam) here.

The package was developed in the context of looking for eukaryotes using marker genes - see [CORRAL](github.com/wbazant/CORRAL) for a packaged workflow. It can also be useful for analysing aligned bacterial reads, e.g. to get quantification outputs.

## Example - detecting eukaryotes

First download the EukDetect reference database following [EukDetect installation instructions](https://github.com/allind/EukDetect).

Then follow this example to download an example metagenomic file, run alignments to a reference database bundled with EukDetect, and obtain a profile using suitable filtering options:

```
REFDB_LOCATION="eukdb"

wget "ftp.sra.ebi.ac.uk/vol1/fastq/ERR274/009/ERR2749179/ERR2749179_1.fastq.gz"
wget "ftp.sra.ebi.ac.uk/vol1/fastq/ERR274/009/ERR2749179/ERR2749179_2.fastq.gz"
gunzip *gz
FASTQ_1="ERR2749179_1.fastq"
FASTQ_2="ERR2749179_2.fastq"

bowtie2 --omit-sec-seq --no-discordant --no-unal \
  -x $REFDB_LOCATION/ncbi_eukprot_met_arch_markers.fna \
  -k10,10
  -1 ERR2749179_1.fastq.gz \
  -2 ERR2749179_2.fastq.gz \
  -S ERR2749179.sam 

FILTERING_OPTS="--min-read-query-length 60 --min-taxon-num-markers 2 --min-taxon-num-reads 2 --min-taxon-better-marker-cluster-averages-ratio 1.01 --threshold-avg-match-identity-to-call-known-taxon 0.97  --threshold-num-taxa-to-call-unknown-taxon 1 --threshold-num-markers-to-call-unknown-taxon 4     --threshold-num-reads-to-call-unknown-taxon 8"

marker_alignments --input ERR2749179.sam --output ERR2749179.taxa.tsv \
  --refdb-format eukprot \
  --refdb-marker-to-taxon-path $REFDB_LOCATION/busco_taxid_link.txt \
  --output-type taxon_all \
  --num-reads $(grep -c '^@' $FASTQ_1) \
  $FILTERING_OPTS
```

## Filtering options

### Bacteria
Recommended setting for bacteria is: `--min-read-query-length 60 --min-taxon-num-reads 100` - only use alignments of length at least 60, report organisms with at least a hundred aligned reads.

### Eukaryotes
Recommended presets for eukaryotes are:

`" --min-read-mapq 30 --min-read-query-length 60 --min-read-match-identity 0.9 --min-taxon-num-markers 2"`
if using single best alignment per query.


If using multiple alignments, the following preset recommended if you're okay with relying on MCL clusters:
` --min-read-query-length 60 --min-taxon-num-markers 2 --min-taxon-num-reads 2 --min-taxon-better-marker-cluster-averages-ratio 1.01 --threshold-avg-match-identity-to-call-known-taxon 0.97  --threshold-num-taxa-to-call-unknown-taxon 1 --threshold-num-markers-to-call-unknown-taxon 4     --threshold-num-reads-to-call-unknown-taxon 8`

A simpler alternative is 
` --min-read-query-length 60 --min-taxon-num-markers 2 --min-taxon-num-reads 2 --min-taxon-fraction-primary-matches 0.5` 
but it does not deal with unknown taxa quite as well.

All filtering options are as follows:

| column | description |
| ------------- | ------------- | 
|`--min-read-mapq`                                   |when reading the input, skip alignments with MAPQ < min-read-mapq                                                                                                                                               |
|`--min-read-query-length`                           |when reading the input, skip alignments shorter than min-read-query-length                                                                                                                                      |
|`--min-read-match-identity`                         |when reading the input, skip alignments where the proportion of matching bases in the alignment is less than min-read-match-identity                                                                            |
|`--min-taxon-num-markers`                           |Only keep taxa with at least min-taxon-num-markers markers                                                                                                                                                      |
|`--min-taxon-num-reads`                             |Only keep taxa with at least min-taxon-num-reads reads                                                                                                                                                          |
|`--min-taxon-num-alignments`                        |Only keep taxa with at least min-taxon-num-alignments alignments                                                                                                                                                          |
|`--min-taxon-fraction-primary-matches`              |Only keep taxa where no more than min-taxon-fraction-primary-matches fraction of alignments is inferior / secondary                                                                                             |
|`--min-taxon-better-marker-cluster-averages-ratio`  |Only keep taxa where the ratio between markers which have at least average match identity relative to their clusters and markers with identity below average is at least min-taxon-better-cluster-averages-ratio|
|`--threshold-avg-match-identity-to-call-known-taxon`|Threshold on average match identity to return taxon in reference                                                                                                                                                |
|`--threshold-num-reads-to-call-unknown-taxon`       |To positively identify an unknown taxon (fits all criteria except match identity) expect this many reads from a taxon cluster                                                                                   |
|`--threshold-num-markers-to-call-unknown-taxon`     |To positively identify an unknown taxon (fits all criteria except match identity) expect this many markers from a taxon cluster                                                                                 |
|`--threshold-num-taxa-to-call-unknown-taxon`     |To positively identify an unknown taxon (fits all criteria except match identity) expect this many taxa from a taxon cluster                                                                                 |
### Reasons to apply filters

1. Very short alignments do not convey useful information
Our ancestors had to make do with 35-40bp shotgun reads, but we have longer ones - game changer for metagenomics! Still, a 100bp read can match on the last twenty bases at the end of a reference sequence (clipped alignments) or you could have configured the aligner to do local alignments instead of end-to-end. Either way, `--min-read-query-length` being something high enough (60 from EukDetect seems to work fine) addresses this problem.

2. Low identity matches are not taxon specific
An unknown species will match as a mixture of results. The clustering option `--min-taxon-better-marker-cluster-averages-ratio` tries to take care of removing the overall inferior evidence, and the `--threshold-avg-match-identity-to-call-known-taxon` only passes

The suggested value of 0.97 has been chosen empirically. Is a bit lower than CCMetagen's 0.9841 quoted from [Vu et al (2019)](https://pubmed.ncbi.nlm.nih.gov/29955203/), as this number was calculated from ribosomal subunits, we're not aware of a study that calculates average identity for BUSCOs. Most unknown taxa seem to match at around 0.9 identity, and a value 0.95 still permitted an unknown <i>Penicillinum</i> species to appear as a mixture.

3. Threshold of evidence for making claims
Claiming a eukaryote is present based on one read would be preposterous! It's not clear how many reads are "enough" to make a claim, and actually, no number of reads is enough because off-target matches follow patterns. We suggest gaining evidence from at least two markers, and a higher standard for ambiguous hits coming from species not in the reference. You can also only report unknown species if the results indicate its two nearest taxa with `--threshold-num-taxa-to-call-unknown-taxon` option.

## Outputs

### Output types
The default option is coverage To get most outputs, set `--output_type taxon_all` for aggregated outputs, or `--output_type marker_all` for the breakdown. See `marker_alignments --help` for other available options.

### Quantification

**Coverage per marker**
= number of reads aligned to the marker times read length divided by length of a marker

**Coverage per taxon**
= average coverage between all markers with nonzero coverage

**CPM (copies per million)** 
= taxon coverage divided by total number of reads and multiplied by one million

CPMs are the most useful number for comparing between different taxa and across samples, since they correct for different sequencing depth between samples, and different reference length between taxa.

Please note that quantitative information might be unreliable when there is very few reads.

## Custom use

### Reference databases
For each reference database, we need to know what taxon each contig or marker sequence is for. This can be provided externally, through a lookup table with the `--refdb-marker-to-taxon-path` option, but we also try support all reference databases of interest to our users through the --refdb-format option. If `--refdb-format generic` produces errors for you, please open a ticket with the details about the reference database and the raised error.

### Additional output options
You can save an intermediate database produced by providing the `--sqlite-db-path` argument, and then query it with a `sqlite3` client.

## How to cite
Please cite our Microbiome publication, https://doi.org/10.1186/s40168-023-01505-1 .

