import os, json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

SUBSTITUTION_MATRICES = ["PAM30", "PAM70", "PAM250",
                         "BLOSUM45", "BLOSUM62", "BLOSUM80"]
WORD_SIZES      = [2,3,4,6]
NUM_WORKERS     = 8

OUTPUT_DIR      = "blast_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DBS     = {"arch": "database/arch_db",
           "euk":  "database/euk_db"}

QUERIES = {"arch": "fasta_files/arch.fasta",
           "euk":  "fasta_files/euk.fasta"}

def blastp(query_file, db_name, out_txt, matrix, word_size):
    cmd = [
        "blastp",
        "-query",   query_file,
        "-db",      db_name,
        "-out",     out_txt,
        "-matrix",  matrix,
        "-word_size", str(word_size),
        "-outfmt",  "6 qseqid sseqid bitscore"
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"[ERROR] BLAST failed on {out_txt}:\n{proc.stderr}", file=sys.stderr)
    return proc.returncode == 0


def run_one(dataset, matrix, word_size) :
    query   = QUERIES[dataset]
    db      = DBS[dataset]
    stem    = f"{dataset}_{matrix}_{word_size}"
    txt_out = os.path.join(OUTPUT_DIR, f"{stem}.txt")


    print(f"[START] {stem}.txt")
    blastp(query, db, txt_out, matrix, word_size)


if __name__ == "__main__":
    tasks = []
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as pool:
        for dataset in DBS:
            for matrix in SUBSTITUTION_MATRICES:
                for w in WORD_SIZES:
                    tasks.append(pool.submit(run_one, dataset, matrix, w))

        for fut in as_completed(tasks):
            path = fut.result()
            print(f"wrote {path}")

    print("\nAll BLAST jobs completed.")
