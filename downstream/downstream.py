import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


FDR = 0.05
paper_genes = {"ABCC5","CRNDE","UQCC","GUSBP11","ANKHD1","ADAM12"}

# OUT-FILES
rmats_dir = Path("results/rmats")

out_results  = Path("downstream/our_results_FDR05.txt")
out_summary = Path("downstream/venn_summary.txt")
out_venn_png = Path("downstream/figures/venn_diagram.png")
out_venn_png.parent.mkdir(parents=True, exist_ok=True)

results = set()

for fp in rmats_dir.glob("*.MATS.JC.txt"): #input data -> JC or JCEC
    if not fp.exists():
        continue

    df = pd.read_csv(fp, sep="\t", dtype=str) #read input 
    df["FDR"] = pd.to_numeric(df["FDR"], errors="coerce")

    gene_col = "geneSymbol" if "geneSymbol" in df.columns else "GeneID"
    sub = df[df["FDR"] < FDR] #0.05 

    genes = set(sub[gene_col].dropna().astype(str))
    results |= (genes & paper_genes)  

out_results.write_text("\n".join(sorted(results)) + "\n", encoding="utf-8")
print("Our target hits:", sorted(results))



###### ANALYSIS #######

overlap = paper_genes & results 
print("Overlap genes:", sorted(overlap))
print("Paper-only genes:", sorted(paper_genes - results))

# Out File 
with open(out_summary, "w", encoding="utf-8") as f:
    f.write(f"FDR cutoff: {FDR}\n")
    f.write(f"Paper targets: {sorted(paper_genes)}\n")
    f.write(f"Our Results: {sorted(results)}\n")
    f.write(f"Overlap: {sorted(overlap)}\n")
    f.write(f"Paper-genes: {sorted(paper_genes - results)}\n")


# Venn Diagram 
fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(1,1,1)

# settings of diagram 
plt.scatter(x=[0,0.25], y=[0,0], s=150000, color=["red","green"], alpha=0.3)
plt.xlim(-0.25,0.5) 
plt.ylim(-0.2, 0.2)
plt.axis("off")

# Text / Numbers
plt.text(x=-0.08, y=0.00, s=str(len(paper_genes - results)), fontsize=28, fontweight="bold", ha="center", va="center")
plt.text(x=0.125, y=0.00, s=str(len(overlap)),    fontsize=28, fontweight="bold", ha="center", va="center")
plt.text(x=0.33,  y=0.00, s=str(len(results - paper_genes)),   fontsize=28, fontweight="bold", ha="center", va="center")

plt.text(x=0.00,  y=0.10, s="Paper (6 genes)", fontsize=16, ha="center")
plt.text(x=0.25,  y=0.10, s="Our results",        fontsize=16, ha="center")

plt.title("Paper vs Our results (FDR < 0.05)", fontsize=35)

plt.tight_layout()
plt.savefig(out_venn_png, dpi=300, bbox_inches="tight")
plt.close(fig)