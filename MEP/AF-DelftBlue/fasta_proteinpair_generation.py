# this script uses a fasta file with all protein sequences that you want to run on alpha fold and
# creates seperate fasta files for all possible pairs (it takes all unique combinations including every protein as a dimer).

from Bio import SeqIO
import itertools
import os
import sys

inFile = sys.argv[1]
outdir = sys.argv[2]

def generate_fasta_pairs(fasta_file, output_dir):
    # Parse the input FASTA file
    sequences = list(SeqIO.parse(fasta_file, "fasta"))

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate all combinations of the sequences
    all_combinations = list(itertools.combinations(sequences, 2))

    # Add self-pairs (if you want every protein paired with itself too)
    self_combinations = [(seq, seq) for seq in sequences]
    all_combinations.extend(self_combinations)

    # Write each pair to a separate FASTA file
    for idx, (seq1, seq2) in enumerate(all_combinations, 1):
        filename = os.path.join(output_dir, f"pair_{idx}_{seq1.id}_{seq2.id}.fasta")
        with open(filename, "w") as output_handle:
            SeqIO.write([seq1, seq2], output_handle, "fasta")
        print(f"Written {seq1.id} and {seq2.id} to {filename}")


# Example usage
#fasta_file = "proteins.fasta"  # Replace with the path to your input FASTA file
#output_dir = "fasta"  # Replace with your desired output directory
generate_fasta_pairs(inFile, outdir)