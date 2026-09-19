<a name="readme-top"></a>

# NeuroProtein Analyzer

A Python based bioinformatics pipeline for exploring sequence derived properties of neurodegenerative disease proteins and comparing them against housekeeping control proteins.

## About The Project

NeuroProtein Analyzer automates the retrieval and analysis of protein sequences associated with major neurodegenerative disorders.

Using Biopython's Entrez and ProtParam modules, the pipeline fetches protein sequences from NCBI, extracts physicochemical and structural features, tests for statistically significant differences between groups, and generates visualizations for exploratory analysis.

The project focuses on five disease associated proteins:

* APP (Amyloid Precursor Protein)
* MAPT (Tau)
* SNCA (Alpha-Synuclein)
* HTT (Huntingtin)
* TARDBP (TDP-43)

and compares them against a curated panel of housekeeping control proteins.

### Built With

* Python
* Biopython
* Pandas
* SciPy
* Matplotlib
* Seaborn
* NCBI Entrez

## Features

* Automated protein sequence retrieval from NCBI
* Physicochemical property analysis using ProtParam
* Disease vs control protein comparison
* Statistical significance testing (Welch's t-test) between groups
* Amino acid composition analysis
* Correlation analysis of protein properties
* Automated table generation
* Exploratory data visualizations

## Workflow

```text
Gene Panel
    ↓
NCBI Sequence Retrieval
    ↓
Protein Sequences
    ↓
ProtParam Analysis
    ↓
Feature Extraction
    ↓
Summary Tables
    ↓
Significance Testing
    ↓
Visualizations
```

## Project Structure

```text
NeuroProtein-Analyzer
│
├── data/
│   └── gene_panel.json
│
├── results/
│   ├── figures/
│   │   ├── aromaticity.png
│   │   ├── correlation_matrix.png
│   │   ├── gravy.png
│   │   ├── instability_index.png
│   │   ├── normalized_aa_heatmap.png
│   │   └── protein_length.png
│   │
│   └── tables/
│       ├── protein_details.csv
│       ├── summary_stats.csv
│       └── significance_stats.csv
│
├── src/
│   ├── analyze.py
│   ├── fetch.py
│   ├── significance.py
│   └── visualize.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Results

The pipeline generates:

* Protein length comparisons
* Instability index distributions
* GRAVY score comparisons
* Aromaticity comparisons
* Correlation matrices
* Amino acid composition heatmaps
* Statistical significance tests (Welch's t-test) for each physicochemical and structural property

### Correlation Matrix

The correlation matrix highlights relationships between sequence-derived protein properties, including protein length, molecular weight, hydrophobicity, instability and predicted secondary structure composition.

![Correlation Matrix](./results/figures/correlation_matrix.png)

### Amino Acid Composition Heatmap

Normalized amino acid frequencies reveal differences in sequence composition across disease and control proteins independent of protein length.

![Amino Acid Heatmap](./results/figures/normalized_aa_heatmap.png)

### Statistical Significance Testing

Each physicochemical and structural property was compared between the disease and control groups using an independent two-sample Welch's t-test (which does not assume equal variance between groups — a safer default for small biological samples).

| Property | Disease Mean | Control Mean | p-value | Significant (p<0.05) |
|---|---|---|---|---|
| Beta structure fraction | 0.298 | 0.369 | 0.028 | **Yes** |
| GRAVY | -0.492 | -0.127 | 0.046 | **Yes** |
| Aromaticity | 0.055 | 0.084 | 0.062 | No (borderline) |
| Instability index | 42.641 | 29.382 | 0.084 | No |
| Alpha structure fraction | 0.336 | 0.312 | 0.497 | No |
| Turn structure fraction | 0.314 | 0.286 | 0.459 | No |
| Isoelectric point | 5.858 | 6.145 | 0.760 | No |
| Molecular weight | 107969.3 | 37358.5 | 0.312 | No |
| Protein length | 981.8 | 339.2 | 0.308 | No |

Full results: [`results/tables/significance_stats.csv`](./results/tables/significance_stats.csv)

### Key Observations

For the selected protein panel:

* Disease proteins showed a significantly lower beta-sheet structure fraction than controls (p = 0.028) — a difference not evident from summary statistics alone.
* Disease proteins showed significantly lower GRAVY scores than controls (p = 0.046), indicating greater hydrophilicity.
* Disease proteins trended toward higher instability indices than controls, but this difference did not reach statistical significance at this sample size (p = 0.084).
* Disease proteins trended toward lower aromaticity than controls, borderline but not statistically significant (p = 0.062).
* Disease proteins exhibited a higher average protein length than the control panel; however, this difference was not statistically significant and was driven largely by HTT, an extreme outlier with a length of over 3000 amino acids.
* Amino acid composition varied considerably across proteins.

These findings are exploratory and based on a small curated dataset (n = 5 per group); non-significant trends should be interpreted cautiously and may reflect limited statistical power rather than an absence of a true effect.

## Getting Started

### Installation

```bash
pip install biopython pandas scipy matplotlib seaborn
```

### Run

```bash
python main.py
```

Generated figures are saved to:

```text
results/figures/
```

Generated tables are saved to:

```text
results/tables/
```

## Limitations

* Small protein panel (5 disease proteins and 5 control proteins) limits statistical power
* Analysis limited to sequence-derived features
* No structural or interaction data included
* Results should be interpreted as exploratory

## Future Work

* Expand the disease and control protein panels to improve statistical power
* Incorporate AlphaFold structural features
* Apply multiple-testing correction (e.g. Benjamini-Hochberg) as the property panel grows
* Include protein interaction network analysis
* Build an interactive visualization dashboard

## Acknowledgments

* NCBI Entrez
* Biopython
* SciPy
* ProtParam

<p align="right">(<a href="#readme-top">back to top</a>)</p>