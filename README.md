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
