import os
import pandas as pd

# Specify the directory containing the PDB files
pdb_dir = 'C:/Users/rensk/OneDrive/Documenten/studie/afstuderen/data/PH_pdbs/'


# Get the list of PDB files in the directory
identifiers = [file for file in os.listdir(pdb_dir) if file.endswith('.pdb')]


# Initialize an empty DataFrame with the identifiers as both columns and index
rmsd_table = pd.DataFrame(columns=identifiers, index=identifiers)

# Open the Pymol output file
file_path = 'Pymol_output_PH_RMSD_all_vs_all_v2.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

# Process each line in the file
for line in lines:
    line = line.strip()
    # If the line does not start with '(', it contains the reference and aligned identifiers
    if line[0] != '{':
        ref = line.split(',')[0][1:].strip('>')
        alg = line.split(',')[1]
    # If the line starts with '{', it contains the RMSD after refinement
    else:
        rmsd= line.split(',')[1][1:]
        print(rmsd)
        rmsd_after_refinement = round(float(rmsd.split(':')[1]), 2)
        print(rmsd_after_refinement)
        rmsd_table.at[alg, ref] = rmsd_after_refinement

# Save the RMSD table to an Excel file
output_file = 'RMSD_PH_models_RMSD_after_refinement2.xlsx'
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    rmsd_table.to_excel(writer, 'Sheet1')
    worksheet = writer.sheets['Sheet1']
    worksheet.set_column(0, len(identifiers), 12)  # Adjust column width for better readability
    worksheet.hide_gridlines()  # Hide gridlines for a cleaner look

# Display the DataFrame (optional, for verification)
print(rmsd_table)
