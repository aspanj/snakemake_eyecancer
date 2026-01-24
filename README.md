# Project
The goal is to automate a pipeline with Snakemake that analyzes sequenced RNA data from patients with uveal melanoma.

The results of the study F3B1 mutations are associated with alternative splicing in uveal melanoma
(https://pubmed.ncbi.nlm.nih.gov/23861464/) should be reproduced.

The following tools were used for the analysis in the study:
- Alignment: TopHat
- Differential splicing analysis: DEXSeq & MATS
→ they trimmed the RNA-seq data to 99bp

We on the other hand did use these tools:
- Alignment: STAR
- Differential splicing analysis: rMATS
→ we trimmed the RNA-seq data to 101bp

The study found differential splicing in the following genes:
- ABCC5
- CRNDE
- UQCC
- GUSBP11
- ANKHD1
- ADAM12

Our results are as follows:
…

# Snakefile
This Snakefile describes a bioinformatic pipeline for RNA-Seq analysis that focuses specifically on the detection of differential splicing (splicing variants).

Explanation of the individual steps in the workflow:

## 1. Configuration & Input
• Configuration: 
The pipeline reads settings from config/config.yaml and sample information from config/samples.tsv.
• Samples: 
The sample list is used to define file paths (r1_path, r2_path) and group affiliations 

## 2. Quality control & preprocessing
The workflow begins with checking and cleaning the raw data:
• Quality check (FastQC): (rule fastqc_raw)
• Trimming (FastP): (rule fastp)

→ Generates trimmed FASTQ files and JSON/HTML reports.

## 3. Alignment (mapping)
The trimmed reads are mapped against the reference genome:
• Index creation: (rule star_index)
Creates a one-time index for the STAR aligner from the reference genome(FASTA) and annotation (GTF).
• Mapping: (rule star_map)
Uses STAR to align the reads.

Important: TwopassMode Basic is used. This is crucial for splicing analyses, as
STAR detects splice junctions in the first pass and uses them in the second pass to
improve the alignment.

→ The output is BAM files sorted by coordinates.

## 4. Summary report
• MultiQC: (rule multiqc)
Collects all reports from FastQC, FastP, and STAR and combines them into a single HTML file (multiqc_report.html) so that you can quickly see whether everything worked technically.

## 5. Splicing analysis
• rMATS: (rule rmats)
→ This is the actual analysis step for alternative splicing.
Grouping: A Python function (bam_list) automatically sorts the BAM files into two groups: "MUT" (mutant/treated) and "WT" (wildtype/control), based on the group column in samples.tsv.

Analysis: rMATS compares these two groups to find significant differences in various
splicing events.

→ Outputs: Text files are generated for five different splicing types:
1. SE: Skipped Exon (exon skipping)
2. A5SS: Alternative 5' splice site
3. A3SS: Alternative 3' splice site
4. MXE: Mutually Exclusive Exons
5. RI: Retained Intron


# Snakemake_Eye_Cancer

1. Jan - Workflow Architect & Data (Git & QC) 🏗️
    Setzt das Git-Repo auf (Struktur, .gitignore).
    Erstellt die samples.tsv (Input-Daten sauber definieren).
    Implementiert FastQC/MultiQC in Snakemake.
    Ziel: Saubere Ordnerstruktur und Qualitätscheck der Rohdaten.

2. Jan - The Mapper (Alignment & Resources) 🧬
    Schreibt Rules für den Download von Genom & Annotation (wichtig für Splicing!).
    Erstellt den STAR-Index und die Mapping-Rule.
    Ziel: Die BAM-Files, die wir für die Analyse brauchen.

3. Luca - Splicing Analyst (Core Logic) ⚙️
    Kümmert sich um das Herzstück: Das Splicing-Tool (z.B. rMATS/MAJIQ).
    Schreibt die Snakemake-Rule für den Vergleich (Mutated vs. WT).
    Ziel: Die rohen Ergebnistabellen (Inclusion Levels/P-Values).

4. Leona - Downstream Investigator (Report & Plots) 📊
    Schreibt das R-Markdown/Jupyter Notebook.
    Filtert die Ergebnisse nach unseren 6 Ziel-Genen (ABCC5, CRNDE, etc.).
    Erstellt die Grafiken (Volcano Plots, Boxplots) für den finalen Report.
    Ziel: Der "Self-contained Report" (Deliverable).

5. Anja & Marion - Integrator & Reproducibility (Docs & Testing) 📝
    Schreibt die README (Wie führt man es aus?).
    Verwaltet die Conda Environments (envs/*.yaml), damit die Versionen stimmen.
    Macht den "Fresh Clone Test": Prüft, ob alles auf einem fremden PC ohne Fehler durchläuft.
    Ziel: Sicherstellen, dass wir volle Punktzahl für Reproduzierbarkeit kriegen.


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
