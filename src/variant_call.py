import subprocess, os
 
 
def call_variants(genome_fasta, bam_path, out_dir="./results/tables"):
    os.makedirs(out_dir, exist_ok=True)
    vcf_path = os.path.join(out_dir, "variants.vcf")
 
    print("Calling variants...")
    mpileup = subprocess.Popen(
        ["bcftools", "mpileup", "-f", genome_fasta, bam_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    with open(vcf_path, "w") as out_f:
        subprocess.run(
            ["bcftools", "call", "-mv", "-Ov"],
            stdin=mpileup.stdout,
            stdout=out_f,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    mpileup.stdout.close()
 
    n_variants = sum(1 for line in open(vcf_path) if not line.startswith("#"))
    print(f"{n_variants} raw variants called.")
 
    return vcf_path
 
 
def filter_variants(vcf_path, min_qual=100, out_dir="./results/tables"):
    os.makedirs(out_dir, exist_ok=True)
    filtered_path = os.path.join(out_dir, "variants.filtered.vcf")
 
    subprocess.run(
        ["bcftools", "view", "-e", f"QUAL<{min_qual}", vcf_path, "-o", filtered_path],
        check=True,
        stderr=subprocess.DEVNULL,
    )
 
    n_filtered = sum(1 for line in open(filtered_path) if not line.startswith("#"))
    print(f"{n_filtered} variants passed QUAL > {min_qual} filter.")
 
    return filtered_path
 
 
if __name__ == "__main__":
    vcf = call_variants("./data/genome.fasta", "./data/aligned.sorted.bam")
    filtered = filter_variants(vcf)
    print("Done. Filtered VCF at:", filtered)
 
