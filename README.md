# Project
The goal is to automate a pipeline with Snakemake that analyzes sequenced RNA data from patients with uveal melanoma.

The results of the study F3B1 mutations are associated with alternative splicing in uveal melanoma
(https://pubmed.ncbi.nlm.nih.gov/23861464/) should be reproduced.

Data is coming from Harbour et al. (ecurrent mutations at codon 625 of the splicing factor
SF3B1 in uveal melanoma - https://pubmed.ncbi.nlm.nih.gov/23313955/). They performed RNA sequencing on ological samples
of patients suffering from uveal melanoma. Data was downloaded from NCBI (https://www.ncbi.nlm.nih.gov/sra/?term=SRA062359)

The following tools were used for the analysis in the study:
- Alignment: TopHat
- Differential splicing analysis: DEXSeq & MATS

→ they trimmed the RNA-seq data to 99bp

We on the other hand did use these tools:
- Alignment: STAR
- Differential splicing analysis: rMATS

The study found differential splicing in the following genes:
- ABCC5
- CRNDE
- UQCC
- GUSBP11
- ANKHD1
- ADAM12

In comparison we only found:
- ANKHD1

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

This is the actual analysis step for alternative splicing.
Grouping: A Python function (bam_list) automatically sorts the BAM files into two groups: "MUT" (mutant/treated) and "WT" (wildtype/control), based on the group column in samples.tsv.

Analysis: rMATS compares these two groups to find significant differences in various
splicing events.

→ Outputs: Text files are generated for five different splicing types:
1. SE: Skipped Exon (exon skipping)
2. A5SS: Alternative 5' splice site
3. A3SS: Alternative 3' splice site
4. MXE: Mutually Exclusive Exons
5. RI: Retained Intron

## 6. Downstream Analysis
• Custom Python Script: (rule downstream_analysis)

This step performs post-processing, filtering, and visualization of the raw rMATS results generated in the previous step.

Processing: The custom Python script (downstream/downstream.py) is executed within a specific environment (envs/downstream.yaml). It reads the "*.MATS.JC.txt" output files from rMATS to identify significant splicing events and compare it to the paper findings.

→ Outputs:

1. Visuals: venn_diagram.png (displays overlap of significant genes of the paper with ours).

2. Filtered Data: our_results_FDR05.txt

3. Summary: venn_summary.txt (describing the results shown in the Venn Diagram)


```
