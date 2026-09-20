from src.fetch import fetch_data
from src.qc import run_fastqc, run_fastp
from src.align import build_index, align_reads
from src.variant_call import call_variants, filter_variants
from src.annotate import annotate_variants
 
paths = fetch_data()
 
run_fastqc([paths["R1.fastq.gz"], paths["R2.fastq.gz"]])
trimmed = run_fastp(paths["R1.fastq.gz"], paths["R2.fastq.gz"])
 
index = build_index(paths["genome.fasta"])
bam = align_reads(index, trimmed["R1_trimmed"], trimmed["R2_trimmed"])
 
vcf = call_variants(paths["genome.fasta"], bam)
filtered_vcf = filter_variants(vcf)
 
annotated = annotate_variants(filtered_vcf, paths["genes.gtf"])
print(annotated.sort_values("qual", ascending=False).head(10))
print(f"\nPipeline complete. {len(annotated)} annotated variants saved to results/tables/")
