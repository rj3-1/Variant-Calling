# NGS Variant Calling Pipeline

A Python-based pipeline for quality control, alignment, and variant calling
from paired-end sequencing reads, with automated annotation against gene
coordinates.

## About

Runs the standard NGS analysis workflow end-to-end: raw reads are fetched,
quality-checked and trimmed, aligned to a reference genome, variant-called,
and the resulting variants are annotated against known gene locations.

Built and tested on a small *Saccharomyces cerevisiae* (yeast) RNA-seq test
dataset (NCBI GEO accession GSE110004, hosted via nf-core/test-datasets),
chosen for its small size, real biological origin, and public availability.
The same pipeline applies directly to other organisms and datasets, including
human sequencing data, given the appropriate reference genome and annotation.

### Built With

* Python
* HISAT2
* samtools
* bcftools
* FastQC
* fastp
* Pandas

## Workflow

```text
Fetch (reads, reference genome, annotation)
    ↓
Quality Control (FastQC) + Trimming (fastp)
    ↓
Alignment (HISAT2) → sorted, indexed BAM
    ↓
Variant Calling (bcftools mpileup + call)
    ↓
Filtering (QUAL threshold)
    ↓
Annotation (variants mapped to overlapping genes)
```

## Project Structure

```text
NGS-Variant-Pipeline
│
├── data/                     (created on run; not committed - see .gitignore)
│
├── results/
│   ├── qc_raw/                FastQC reports on raw reads
│   └── tables/
│       ├── variants.vcf               raw variant calls
│       ├── variants.filtered.vcf      quality-filtered variants
│       └── variants_annotated.csv     variants with overlapping gene names
│
├── src/
│   ├── fetch.py               downloads reads, reference genome, annotation
│   ├── qc.py                  FastQC + fastp trimming
│   ├── align.py                HISAT2 indexing + alignment
│   ├── variant_call.py         bcftools variant calling + filtering
│   └── annotate.py             maps variants to overlapping genes
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Results

Running the pipeline on the test dataset produced 156 raw variant calls,
64 of which passed a QUAL > 100 filter. Two notable findings from
annotation:

* Multiple high-confidence variants map to **SSA1**, a well-characterized
  cytosolic Hsp70 molecular chaperone essential for protein folding and the
  cellular stress response.
* A dense cluster of variants maps to **YAR009C**, a Ty1 retrotransposon
  gag-pol gene. Reads from multiple genomic copies of the repetitive element
  mapping to a single reference copy. This is a well documented artefact in
  repetitive-element analysis rather than genuine single-locus variation.
  

## Getting Started

### Installation

```bash
pip install -r requirements.txt
```

The pipeline also requires the following command-line tools to be
installed separately:

* FastQC
* fastp
* HISAT2
* samtools
* bcftools

On Ubuntu/WSL:
```bash
sudo apt-get install fastqc fastp hisat2 samtools bcftools
```

### Run

```bash
python main.py
```

## Limitations

* Built and tested on yeast test data; not a human/disease dataset
* Variant calling on RNA-seq (rather than DNA-seq) data has known limitations
  around splice-junction artefacts and coverage bias
* Small dataset size limits statistical power of variant calls

## Future Work

* Apply the same pipeline to a DNA-seq dataset for cleaner variant calls
* Add read-depth visualisation across the genome
* Extend annotation to include predicted amino-acid change for coding variants

## Acknowledgments

* nf-core/test-datasets
* NCBI GEO (GSE110004)
