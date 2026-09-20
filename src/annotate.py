import pandas as pd
 
 
def load_gtf_transcripts(gtf_path):
    transcripts = []
    with open(gtf_path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.strip().split("\t")
            if len(fields) < 9 or fields[2] != "transcript":
                continue
 
            chrom, start, end, attrs = fields[0], int(fields[3]), int(fields[4]), fields[8]
 
            gene_id = ""
            gene_name = ""
            for attr in attrs.split(";"):
                attr = attr.strip()
                if attr.startswith("gene_id"):
                    gene_id = attr.split('"')[1]
                elif attr.startswith("gene_name"):
                    gene_name = attr.split('"')[1]
 
            transcripts.append((chrom, start, end, gene_id, gene_name))
 
    return transcripts
 
 
def annotate_variants(vcf_path, gtf_path, out_dir="./results/tables"):
    transcripts = load_gtf_transcripts(gtf_path)
 
    rows = []
    with open(vcf_path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.strip().split("\t")
            chrom, pos, ref, alt, qual = fields[0], int(fields[1]), fields[3], fields[4], fields[5]
 
            matched_genes = [
                gene_name if gene_name else gene_id
                for (t_chrom, start, end, gene_id, gene_name) in transcripts
                if t_chrom == chrom and start <= pos <= end
            ]
 
            rows.append({
                "chrom": chrom,
                "position": pos,
                "ref": ref,
                "alt": alt,
                "qual": float(qual),
                "gene": ", ".join(matched_genes) if matched_genes else "intergenic",
            })
 
    df = pd.DataFrame(rows)
    out_path = f"{out_dir}/variants_annotated.csv"
    df.to_csv(out_path, index=False)
 
    return df
 
 
if __name__ == "__main__":
    df = annotate_variants("./results/tables/variants.filtered.vcf", "./data/genes.gtf")
    print(df.sort_values("qual", ascending=False).head(10))
    print(f"\nSaved {len(df)} annotated variants to ./results/tables/variants_annotated.csv")
