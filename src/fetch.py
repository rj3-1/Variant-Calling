import urllib.request, gzip, shutil, os
 
BASE_URL = "https://raw.githubusercontent.com/nf-core/test-datasets/rnaseq"
 
FILES = {
    "R1.fastq.gz": f"{BASE_URL}/testdata/GSE110004/SRR6357070_1.fastq.gz",
    "R2.fastq.gz": f"{BASE_URL}/testdata/GSE110004/SRR6357070_2.fastq.gz",
    "genome.fasta": f"{BASE_URL}/reference/genome.fasta",
    "genes.gtf.gz": f"{BASE_URL}/reference/genes.gtf.gz",
}
 
 
def fetch_data(data_dir="./data"):
    os.makedirs(data_dir, exist_ok=True)
    paths = {}
 
    for filename, url in FILES.items():
        dest = os.path.join(data_dir, filename)
        if os.path.exists(dest):
            print(f"{filename} already exists, skipping download.")
        else:
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, dest)
        paths[filename] = dest
 
    gtf_path = os.path.join(data_dir, "genes.gtf")
    if os.path.exists(gtf_path):
        print("genes.gtf already exists, skipping unzip.")
    else:
        print("Unzipping genes.gtf.gz...")
        with gzip.open(paths["genes.gtf.gz"], "rb") as f_in, open(gtf_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    paths["genes.gtf"] = gtf_path
 
    return paths
 
 
if __name__ == "__main__":
    fetch_data()
    print("Done. Files saved to ./data/")