# rMATS differential splicing (Subject 1)
## rMATS command used

```bash
rmats.py \
  --b1 meta/group_mut.txt \
  --b2 meta/group_wt.txt \
  --gtf ref/genes.gtf \
  --od results_rmats \
  --tmp results_rmats/tmp \
  --readLength 101 \
  -t paired \
  --libType fr-unstranded \
  --nthread 8

Tool: rMATS v4.3.0  
Comparison: SF3B1-mutant (b1) vs wild-type (b2)

IncLevelDifference = MUT - WT

Recommended filters:
- FDR < 0.05
- |ΔPSI| > 0.10

Use *.MATS.JC.txt output files for downstream analysis.
