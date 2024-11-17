import os
from pymol import cmd

def sanitize_name(file_name):
    """Sanitize the PDB file name to create a valid PyMOL selection name."""
    sanitized = file_name.replace('.pdb', '')
    sanitized = ''.join(e for e in sanitized if e.isalnum() or e == '_')
    sanitized = sanitized.strip()  # Remove any trailing whitespace
    if not sanitized[0].isalpha():
        sanitized = 'struct_' + sanitized
    return sanitized

def RMSD_calc():
    home = 'C:/Users/rensk/'
    pdb_dir = 'OneDrive/Documenten/studie/afstuderen/data/PH_pdbs/'

    # Get a list of all PDB files in the directory
    pdb_files = [f for f in os.listdir(os.path.join(home, pdb_dir)) if f.endswith('.pdb')]

    for j in range(len(pdb_files)):
        pdb_id_ref = pdb_files[j]
        pdb_file_ref = os.path.join(home, pdb_dir, pdb_id_ref)
        sanitized_ref = sanitize_name(pdb_id_ref)

        for k in range(len(pdb_files)):
            pdb_id_alg = pdb_files[k]
            pdb_file_alg = os.path.join(home, pdb_dir, pdb_id_alg)
            sanitized_alg = sanitize_name(pdb_id_alg)

            try:
                cmd.load(pdb_file_ref, sanitized_ref)  # Load the reference PDB file into PyMOL with sanitized name
                cmd.load(pdb_file_alg, sanitized_alg)  # Load the PDB file to align with the reference with sanitized name
                cmd.hide('everything', sanitized_ref)  # Hide the reference structure
                cmd.hide('everything', sanitized_alg)  # Hide the aligned structure

                # Align the two structures using the CE algorithm and get alignment info
                alg_info_list = cmd.cealign(target=sanitized_ref, mobile=sanitized_alg, quiet=1)

                # Print the reference ID, aligned ID, and the alignment information
                print('>' + sanitized_ref + ',' + sanitized_alg)
                print(alg_info_list)
                cmd.delete('all')  # Delete all loaded structures from PyMOL

            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except Exception as e:
                print(f"Error processing {sanitized_ref} and {sanitized_alg}: {str(e)}")

    print('Done!')

cmd.extend("RMSD_calc", RMSD_calc)
