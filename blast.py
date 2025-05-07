import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

SUBSTITUTION_MATRICES = ["PAM30", "PAM70", "PAM250", "BLOSUM45", "BLOSUM62", "BLOSUM80"]
WORD_SIZES = [3]
NUM_WORKERS = 8 

OUTPUT_DIR = "blast_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DBS = {
    "arch": "database/arch_db",
    "euk": "database/euk_db"
}

QUERIES = {
    "arch": "fasta_files/arch.fasta",
    "euk": "fasta_files/euk.fasta"
}

def run_blast(dataset, matrix, word_size=3):
    query_file = QUERIES[dataset]
    db_name = DBS[dataset]
    output_filename = f"{dataset}_{matrix}_{word_size}.txt"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    cmd = [
        "blastp",
        "-query", query_file,
        "-db", db_name,
        "-out", output_path,
        "-outfmt", "6 qseqid sseqid evalue bitscore",
        "-matrix", matrix,
        "-word_size", str(word_size)
    ]

    print(f"[STARTING] {output_filename}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print(f"[ERROR] {output_filename} failed:\n{result.stderr.decode()}")
    else:
        print(f"[FINISHED] {output_filename}")
    return output_filename

if __name__ == "__main__":
    tasks = []
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        for dataset in ["arch", "euk"]:
            for matrix in SUBSTITUTION_MATRICES:
                for word_size in WORD_SIZES:
                    tasks.append(executor.submit(run_blast, dataset, matrix, word_size))

        for future in as_completed(tasks):
            result_file = future.result()
            print(f"Done: {result_file}")

    print("\n All parallel BLAST runs completed.")
