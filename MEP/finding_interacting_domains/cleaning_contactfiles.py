import pandas as pd
import os


# Directory containing the input TSV files
input_dir = "C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/contactsAF2"  # Replace with the actual directory path
# Directory to save the output TSV files
output_dir = "C:/Users/rensk/PycharmProjects/MEP_codefiles/MEP/data/list2_data/contactsAF2_unique"  # Replace with the actual directory path

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process each TSV file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.tsv'):
        input_tsv_path = os.path.join(input_dir, filename)
        output_tsv_path = os.path.join(output_dir, filename)

        # Read the TSV file into a DataFrame
        df = pd.read_csv(input_tsv_path, sep='\t')

        # Remove the specified columns
        columns_to_remove = ['Atom1', 'Atom1_Number', 'Atom2', 'Atom2_Number']
        df.drop(columns=columns_to_remove, inplace=True)

        # Remove duplicate rows based on the residue number
        df_unique = df.drop_duplicates(subset=['Residue1_Number', 'Residue2_Number'])

        # Save the resulting DataFrame to a new TSV file
        df_unique.to_csv(output_tsv_path, sep='\t', index=False)

        print(f"Processed {input_tsv_path} and saved unique residues to {output_tsv_path}")

