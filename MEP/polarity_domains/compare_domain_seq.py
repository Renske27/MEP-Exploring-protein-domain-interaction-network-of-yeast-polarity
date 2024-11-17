from Bio import SeqIO
import sys
import os

# inputfiles
input_SH3 = "C:/Users/rensk/OneDrive/Documenten/studie/afstuderen/data/MSA_SH3/clustalo-I20240819-101005-0997-19671141-p1m.fasta"
input_PH ="C:/Users/rensk/OneDrive/Documenten/studie/afstuderen/data/MSA_PH/clustalo-I20240819-100116-0650-80514678-p1m.fasta"


# Function to calculate the average sequence based on the frequency-weighted scoring of amino acids at each position
def calculate_average_sequence(inputfile):
    # Check if the file exists before proceeding
    if not os.path.exists(inputfile):
        print(f"Error: The file {inputfile} does not exist.")
        sys.exit(1)

    # Read sequences from the FASTA file
    sequences = list(SeqIO.parse(inputfile, "fasta"))
    total_sequences = len(sequences)

    # Initialize a dictionary to store counts for each position
    position_aa_counts = {}

    # Count amino acids at each position across all sequences
    for sequence in sequences:
        for index, aa in enumerate(sequence.seq):
            if index not in position_aa_counts:
                position_aa_counts[index] = {}
            if aa not in position_aa_counts[index]:
                position_aa_counts[index][aa] = 0
            position_aa_counts[index][aa] += 1

    # Determine the frequency of the most common amino acid at each position
    average_aa_at_positions = {}
    for index, counts in position_aa_counts.items():
        most_common_aa = max(counts, key=counts.get)
        frequency = counts[most_common_aa] / total_sequences
        average_aa_at_positions[index] = (most_common_aa, frequency)

    # Define the output file to save the scores
    output_file = inputfile.replace('.fasta', '_scored.fasta')

    with open(output_file, 'w') as outfile:
        # Score each sequence based on frequency-weighted matching
        best_score = 0
        most_average_sequence = None
        most_average_sequence_name = None

        for sequence in sequences:
            score = sum(
                average_aa_at_positions[i][1] if i in average_aa_at_positions and aa == average_aa_at_positions[i][
                    0] else 0
                for i, aa in enumerate(sequence.seq))
            # Update sequence ID with score
            sequence.id += f" | Score: {score:.2f}"
            sequence.description = ''  # Clear the description to avoid duplication in output
            SeqIO.write(sequence, outfile, "fasta")
            if score > best_score:
                best_score = score
                most_average_sequence = sequence.seq
                most_average_sequence_name = sequence.id

    return most_average_sequence_name, most_average_sequence, best_score

# Calculate the average sequence for SH3
domain_mostaverage_SH3, seq_domain_mostaverage_SH3 , score_SH3= calculate_average_sequence(input_SH3)
print(f"\nDomain most similar to average: {domain_mostaverage_SH3}\nSequence: {seq_domain_mostaverage_SH3}")

# Calculate the average sequence for PH
domain_mostaverage_PH, seq_domain_mostaverage_PH, score_PH = calculate_average_sequence(input_PH)
print(f"Domain most similar to average: {domain_mostaverage_PH} \nSequence: {seq_domain_mostaverage_PH}")





