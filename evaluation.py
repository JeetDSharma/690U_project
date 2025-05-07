import os
import pandas as pd
from collections import defaultdict

DATASETS = {
    "arch": "datasets/arch_retrieval.csv",
    "euk": "datasets/euk_retrieval.csv"
}

BLAST_RESULTS_DIR = "blast_results"

def load_ground_truth(csv_file):
    df = pd.read_csv(csv_file)
    return dict(zip(df["Entry"], df["Protein names"]))

def parse_blast_output(filepath):
    hit_dict = defaultdict(list)
    with open(filepath, 'r') as f:
        for line in f:
            qseqid, sseqid, *_ = line.strip().split()
            if sseqid not in hit_dict[qseqid]:
                hit_dict[qseqid].append(sseqid)
    return hit_dict

def map_at_k(ground_truth, predictions, k=5):

    avg_precisions = []

    for query_id, predicted_ids in predictions.items():
        true_label = ground_truth.get(query_id)
        if not true_label:
            continue

        score = 0.0
        correct = 0

        for rank, pid in enumerate(predicted_ids[:k], start=1):
            if ground_truth.get(pid) == true_label:
                correct += 1
                score += correct / rank 

        if correct > 0:
            avg_precisions.append(score / min(correct, k))
        else:
            avg_precisions.append(0.0)
    if len(avg_precisions) == 0:
        return 0.0
    return sum(avg_precisions) / len(avg_precisions)

def evaluate_all():
    results = []

    for filename in os.listdir(BLAST_RESULTS_DIR):
        if not filename.endswith(".txt"):
            continue

        parts = filename.replace(".txt", "").split("_")
        dataset = parts[0]
        matrix = parts[1]
        word_size = parts[2]

        blast_file = os.path.join(BLAST_RESULTS_DIR, filename)
        gt = load_ground_truth(DATASETS[dataset])
        predictions = parse_blast_output(blast_file)
        score = map_at_k(gt, predictions, k=5)

        results.append({
            "dataset": dataset,
            "matrix": matrix,
            "word_size": word_size,
            "MAP@5": round(score, 4)
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    df = evaluate_all()
    df.sort_values(by="MAP@5", ascending=False, inplace=True)
    print("\nBLAST Evaluation Results:")
    print(df.to_string(index=False))
    df.to_csv("blast_map5_scores.csv", index=False)
