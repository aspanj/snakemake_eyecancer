# Snakemake_Eye_Cancer

Folder structure:

```
├── .gitignore               # Exclude huge data/results and local configs
├── README.md                # Experimental design, data sources [1][2], and run instructions
├── config/
│   ├── config.yaml          # Global paths, tool parameters (e.g., STAR indices, rMATS/MAJIQ params)
│   ├── samples.tsv          # Metadata defining Group 1 (SF3B1-mut) vs Group 2 (WT)
│   └── units.tsv            # Links FASTQ files to samples (if multiple lanes per sample)
├── workflow/
│   ├── Snakefile            # Main entry point (defines the final target files)
│   ├── envs/                # Conda environment YAMLs (e.g., splicing.yaml, qc.yaml)
│   ├── rules/               # Modularized logic
│   │   ├── common.smk       # Helper functions (e.g., parsing samples.tsv)
│   │   ├── qc.smk           # FastQC, MultiQC
│   │   ├── align.smk        # STAR or HISAT2 alignment logic
│   │   └── splicing.smk     # Differential splicing tools (rMATS, DEXSeq, or LeafCutter)
│   ├── scripts/             # Python/R scripts wrapped by rules (e.g., formatting splicing output)
│   └── schemas/             # JSON schemas to validate config/samples files
├── resources/               # Static biological assets (downloaded once)
│   ├── genome.fa
│   └── annotation.gtf       # Critical for defining exon boundaries
├── results/                 # Pipeline output (Git-ignored)
│   ├── qc/
│   ├── mapped/              # BAM files
│   └── splicing/            # Raw output from splicing tools (e.g., Sashimi plots, inclusion levels)
└── downstream/              # The "Self-contained report" deliverable
    ├── analysis_report.Rmd  # RMarkdown or Jupyter Notebook
    └── figures/             # Final publication-ready plots for ABCC5, CRNDE, etc.
```
