import pandas as pd
import os
from collections import defaultdict
import json
def load_actual_sequences(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    actual_sequences = []
    for entry in data:
        actual_sequences.append({
            "qid": entry["qid"],
            "relevant_sqids": entry["relevant_sqids"]
        })

    return actual_sequences



def load_blast_results_from_file(file_path):

    results = defaultdict(list)

    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("qid") or line.strip() == "":
                continue
            parts = line.strip().split()
            if len(parts) != 3:
                continue
            qid, sqid, bitscore = parts
            results[qid].append({"seqid": str(sqid), "score": float(bitscore)})

    for qid in results:
        results[qid].sort(key=lambda x: -x["score"])

    return results


def calculate_map(ground_truth, blast_results):
    aps = []

    gt_lookup = {item['qid']: set(item['relevant_sqids']) for item in ground_truth}

    for qid, relevant_set in gt_lookup.items():
        if qid not in blast_results:
            continue  

        retrieved = blast_results[qid]
        num_relevant = 0
        precision_at_k = []

        for k, item in enumerate(retrieved, start=1):
            if item['seqid'] in relevant_set:
                num_relevant += 1
                precision = num_relevant / k
                precision_at_k.append(precision)

        if relevant_set:
            ap = sum(precision_at_k) / len(relevant_set)
            aps.append(ap)

    return sum(aps) / len(aps) if aps else 0.0



if __name__ == "__main__":
    k = 5 
    
    SUBSTITUTION_MATRICES = ["PAM30", "PAM70", "PAM250", "BLOSUM45", "BLOSUM62", "BLOSUM80"]

    WORD_SIZES = [2,3,4,6]

    for matrix in SUBSTITUTION_MATRICES:
        for word_size in WORD_SIZES:
            actual_seq_file_arch = f"datasets/arch_actual_seq.json"
            blast_results_dir_arch = f"blast_results/arch_{matrix}_{word_size}.txt"

            ground_seq_arch = load_actual_sequences(actual_seq_file_arch)
            blast_results_arch = load_blast_results_from_file(blast_results_dir_arch)
            map_at_k_arch = calculate_map(ground_seq_arch, blast_results_arch)
            print(f"MAP@{k} for arch with {matrix} and word size {word_size}: {map_at_k_arch:.4f}")

    for matrix in SUBSTITUTION_MATRICES:
        for word_size in WORD_SIZES:
            actual_seq_file_euk = f"datasets/euk_actual_seq.json"
            blast_results_dir_euk = f"blast_results/euk_{matrix}_{word_size}.txt"

            actual_seq_euk = load_actual_sequences(actual_seq_file_euk)
            blast_results_euk = load_blast_results_from_file(blast_results_dir_euk)
            map_at_k_euk = calculate_map(actual_seq_euk, blast_results_euk)
            print(f"MAP@{k} for euk with {matrix} and word size {word_size}: {map_at_k_euk:.4f}")
    # ground_truth = [
    #         {
    #         "qid": "1",
    #         "relevant_sqids": [
    #         "2",
    #         "5"
    #         ]
    #     }
    # ]
    # blast_results = {
    #     "1": [
    #         {"seqid": "2", "score": 100.0},
    #         {"seqid": "3", "score": 90},
    #         {"seqid": "4", "score": 80},
    #         {"seqid": "5", "score": 70},
    #         {"seqid": "6", "score": 60}
    #     ],
    #     "2": [
    #         {"seqid": "5", "score": 100},
    #         {"seqid": "6", "score": 90}
    #     ]
    # }

    # # precision_at_k_result = precision_at_k([1,2], [1,2], 1)
    # map5 = calculate_map(ground_truth, blast_results)
    # print(f"MAP@5: {map5:.4f}")