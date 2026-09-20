import subprocess, os
 
 
def build_index(genome_fasta, index_dir="./data/hisat2_index"):
    os.makedirs(index_dir, exist_ok=True)
    index_prefix = os.path.join(index_dir, "genome")
 
    print("Building HISAT2 index from reference genome...")
    subprocess.run(
        ["hisat2-build", "-p", "4", genome_fasta, index_prefix],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("Index built.")
 
    return index_prefix
 
 
def align_reads(index_prefix, r1, r2, out_dir="./data"):
    os.makedirs(out_dir, exist_ok=True)
    sam_path = os.path.join(out_dir, "aligned.sam")
    bam_sorted = os.path.join(out_dir, "aligned.sorted.bam")
 
    print("Aligning reads to reference...")
    subprocess.run(
        [
            "hisat2", "-p", "4",
            "-x", index_prefix,
            "-1", r1,
            "-2", r2,
            "-S", sam_path,
        ],
        check=True,
    )
 
    subprocess.run(
        ["samtools", "sort", "-@", "4", "-o", bam_sorted, sam_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
 
    subprocess.run(
        ["samtools", "index", bam_sorted],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
 
    print("Alignment complete. Sorted BAM ready.")
    return bam_sorted
 
 
if __name__ == "__main__":
    idx = build_index("./data/genome.fasta")
    bam = align_reads(idx, "./data/R1.trimmed.fastq.gz", "./data/R2.trimmed.fastq.gz")
    print("Done. Sorted BAM at:", bam)
 