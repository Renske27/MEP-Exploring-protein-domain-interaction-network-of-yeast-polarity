import os
from pymol import cmd

# in pymol first cd to directory where file is located
# then --> run <filename>
# then call function --> <functionname>

def sanitize_name(file_name):
    """Sanitize the CIF file name to create a valid PyMOL selection name."""
    sanitized = file_name.replace('_model_0.cif', '')
    sanitized = sanitized.replace('fold_fold_', '')
    sanitized = sanitized.strip()  # Remove any trailing whitespace or special characters
    return sanitized

def RMSD_calc():
    home = 'C:/Users/rensk/'
    cif_dir = 'OneDrive/Documenten/studie/afstuderen/data/alphafold3/rerunned/'

    # Get a list of all cif files in the directory
    cif_files = [f for f in os.listdir(os.path.join(home, cif_dir)) if f.endswith('model_0.cif')]

    for j in range(len(cif_files)):
        cif_id_ref = cif_files[j]
        cif_file_ref = os.path.join(home, cif_dir, cif_id_ref)
        sanitized_ref = sanitize_name(cif_id_ref)

        # Extract protein names from the filename
        protein_names = cif_id_ref.split('_')[3:5]

        for k in range(j + 1, len(cif_files)):
            filename_parts = cif_files[k].split('_')

            if protein_names[0] in filename_parts and protein_names[1] in filename_parts:

                cif_id_alg = cif_files[k]
                cif_file_alg = os.path.join(home, cif_dir, cif_id_alg)
                sanitized_alg = sanitize_name(cif_id_alg)

                #protein_names2 = cif_id_alg.split('_')[3:5]
                #sanitized_alg = '_'.join(protein_names2)


                try:
                    # Load the reference CIF file into PyMOL as a new object
                    cmd.load(cif_file_ref, sanitized_ref, format='cif')
                    # Load the CIF file to align as a new object
                    cmd.load(cif_file_alg, sanitized_alg, format='cif')
                    cmd.hide('everything', sanitized_ref)  # Hide the structures for clarity
                    cmd.hide('everything', sanitized_alg)  # Hide the structures for clarity

                    # Align the two structures using the align command and get alignment info
                    alignment_info = cmd.align(sanitized_ref, sanitized_alg, quiet=1)

                    # Print the reference ID, aligned ID, and the alignment information
                    print('>' + sanitized_ref + ',' + sanitized_alg)
                    print(f"RMSD={alignment_info[0]}, "
                          f"Number of atoms used={alignment_info[1]}, "
                          f"Number of cycles={alignment_info[2]}, "
                          f"RMSD before refinement={alignment_info[3]}, "
                          f"Number of aligned atoms before refinement={alignment_info[4]}")
                    cmd.delete('all')  # Delete all loaded structures from PyMOL

                except IOError as e:
                    print("I/O_error({0}:_{1}".format(e.errno, e.strerror))

            cmd.delete('all')

    print('Done!')

cmd.extend("RMSD_calc", RMSD_calc)
