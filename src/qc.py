import subprocess, os, json
 
 
def run_fastqc(fastq_paths, out_dir="./results/qc_raw"):
    os.makedirs(out_dir, exist_ok=True)
    print(f"Running FastQC on {len(fastq_paths)} file(s)...")
    subprocess.run(
        ["fastqc", *fastq_paths, "-o", out_dir],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("FastQC done.")
    return out_dir
 
 
def run_fastp(r1, r2, out_dir="./data"):
    os.makedirs(out_dir, exist_ok=True)
    r1_trimmed = os.path.join(out_dir, "R1.trimmed.fastq.gz")
    r2_trimmed = os.path.join(out_dir, "R2.trimmed.fastq.gz")
    json_report = os.path.join(out_dir, "fastp.json")
 
    print("Trimming adapters and low-quality bases...")
    subprocess.run(
        [
            "fastp",
            "-i", r1, "-I", r2,
            "-o", r1_trimmed, "-O", r2_trimmed,
            "-j", json_report,
            "-h", os.path.join(out_dir, "fastp.html"),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
 
    with open(json_report) as f:
        report = json.load(f)
    before = report["summary"]["before_filtering"]["total_reads"]
    after = report["summary"]["after_filtering"]["total_reads"]
    print(f"Trimming done: {after}/{before} reads passed filtering.")
 
    return {"R1_trimmed": r1_trimmed, "R2_trimmed": r2_trimmed}
 
 
if __name__ == "__main__":
    run_fastqc(["./data/R1.fastq.gz", "./data/R2.fastq.gz"])
    trimmed = run_fastp("./data/R1.fastq.gz", "./data/R2.fastq.gz")
    print("Done. Trimmed files:", trimmed)
 
