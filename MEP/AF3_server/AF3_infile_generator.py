import itertools
import json
from Bio import SeqIO

# Read the sequences from the FASTA file
fasta_file = "../data/list2_data/fasta_list2.fasta"  # Replace this with the actual path to your fasta file
sequences = []

# Parse the FASTA file and store sequences along with their identifiers
for record in SeqIO.parse(fasta_file, "fasta"):
    sequences.append((record.id, str(record.seq)))

# Generate all combinations of the sequences
all_combinations = list(itertools.product(sequences, repeat=2))

# Create the jobs in the required format
jobs = []
for idx, ((id1, seq1), (id2, seq2)) in enumerate(all_combinations):
    job = {
        "name": f"Fold_{idx + 1}_{id1}_{id2}",
        "modelSeeds": [],
        "sequences": [
            {
                "proteinChain": {
                    "sequence": seq1,
                    "count": 1
                }
            },
            {
                "proteinChain": {
                    "sequence": seq2,
                    "count": 1
                }
            },
        ]
    }
    jobs.append(job)


# Function to write jobs to JSON files with a maximum of 100 jobs per file
def write_jobs_to_files(jobs, max_jobs_per_file=100):
    total_jobs = len(jobs)
    num_files = (total_jobs // max_jobs_per_file) + (1 if total_jobs % max_jobs_per_file else 0)

    for i in range(num_files):
        start_idx = i * max_jobs_per_file
        end_idx = min(start_idx + max_jobs_per_file, total_jobs)
        file_jobs = jobs[start_idx:end_idx]

        output_file = f"jobs_part_{i + 1}.json"
        with open(output_file, "w") as json_file:
            json.dump(file_jobs, json_file, indent=4)
        print(f"Written {len(file_jobs)} jobs to {output_file}")


# Write jobs to multiple JSON files
write_jobs_to_files(jobs)
