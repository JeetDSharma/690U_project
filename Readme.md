# 690U Project: Sequence Retrieval and Evaluation

This project focuses on the retrieval and evaluation of biological sequences using BLAST (Basic Local Alignment Search Tool). We utilize sequence similarity searches to assess functional similarity between proteins.

## Project Structure

- **`blast_results/`**: Output files generated from BLAST searches.
- **`database/`**: BLAST database files used for alignments.
- **`datasets/`**: Datasets used for testing and evaluation.
- **`fasta_files/`**: Input FASTA files containing sequences.
- **`blast.py`**: Script to run BLAST with various parameter settings.
- **`evaluation_test.py`**: Evaluates retrieval performance using MAP@k.
- **`retrieval.ipynb`**: Jupyter notebook for generating the fasta file and actual sequence mappings

## Requirements

- Python 3.x
- Biopython
- NCBI BLAST+ suite

## Usage

Create a BLAST database from the FASTA files:

Or use the notebook for generating the fasta file and actual sequence mappings:
```bash
jupyter notebook retrieval.ipynb
```

```bash
makeblastdb -in arch.fasta -dbtype prot -out database/arch_db
makeblastdb -in euk.fasta -dbtype prot -out database/euk_db
```

Run BLAST for a specific dataset and configuration:
```bash
python blast.py
```

Evaluate BLAST output with MAP@5:
```bash
python evaluation_test.py
```



## Planned Results

We compare our BLAST-based functional retrieval results against the DGEB benchmark. MAP@5 scores are computed for various configurations.

**MAP@5 for arch dataset**
| Substitution Matrix | WS=2   | WS=3   | WS=4       | WS=6   |
| ------------------- | ------ | ------ | ---------- | ------ |
| PAM30               | 0.8151 | 0.7883 | 0.8021     | 0.7443 |
| PAM70               | 0.8465 | 0.8372 | 0.8451     | 0.7895 |
| PAM250              | 0.8617 | 0.8614 | 0.8712     | 0.7877 |
| BLOSUM45            | 0.8782 | 0.8721 | **0.8784** | 0.8522 |
| BLOSUM62            | 0.8667 | 0.8590 | 0.8672     | 0.7795 |
| BLOSUM80            | 0.8726 | 0.8693 | 0.8830     | 0.8013 |

**MAP@5 for arch dataset**
| Substitution Matrix | WS=2   | WS=3   | WS=4       | WS=6   |
| ------------------- | ------ | ------ | ---------- | ------ |
| PAM30               | 0.8482 | 0.8171 | 0.8295     | 0.7653 |
| PAM70               | 0.8754 | 0.8651 | 0.8733     | 0.8092 |
| PAM250              | 0.8912 | 0.8912 | 0.8928     | 0.8103 |
| BLOSUM45            | 0.9062 | 0.8994 | **0.9072** | 0.8751 |
| BLOSUM62            | 0.8877 | 0.8863 | 0.8892     | 0.7965 |
| BLOSUM80            | 0.8892 | 0.8840 | 0.8901     | 0.7850 |

