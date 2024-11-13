import os
import json


def rename_files_in_directory(dir_output):
    # Iterate through all directories in the given directory
    for subdir, dirs, files in os.walk(dir_output):
        for directory in dirs:
            # Construct the path to the current directory
            current_dir = os.path.join(subdir, directory)

            # Search for the ranking_debugged.json file
            ranking_file_path = os.path.join(current_dir, 'ranking_debug.json')
            if os.path.exists(ranking_file_path):
                # Open and read the ranking_debugged.json file
                with open(ranking_file_path, 'r') as ranking_file:
                    ranking_data = json.load(ranking_file)

                # Get the first entry in the order section
                rank0 = ranking_data.get('order', [None])[0]

                if rank0:
                    # Iterate through all files in the current directory
                    for filename in os.listdir(current_dir):
                        if rank0 in filename:
                            # Construct the new filename with the directory name prefixed
                            new_filename = f"{directory}_{filename}"
                            old_file_path = os.path.join(current_dir, filename)
                            new_file_path = os.path.join(current_dir, new_filename)
                            # Rename the file
                            os.rename(old_file_path, new_file_path)
                            print(f"Renamed {filename} to {new_filename} in {current_dir}")

                        elif filename == 'features.pkl' or filename == 'ranked_0.cif' or filename == 'ranking_debug.json' or filename == 'timings.json':
                            # Construct the new filename with the directory name prefixed
                            new_filename = f"{directory}_{filename}"
                            old_file_path = os.path.join(current_dir, filename)
                            new_file_path = os.path.join(current_dir, new_filename)


                            # Rename the file
                            os.rename(old_file_path, new_file_path)
                            print(f"Renamed {filename} to {new_filename} in {current_dir}")


if __name__ == "__main__":
    # Define the output directory
    #dir_output= 'C:/Users/rensk/OneDrive/Documenten/studie/afstuderen/data/alphafold2'
    dir_output = '/scratch/rtukker/AF/output_list2/scratch/rtukker/AF/output_list2'  # Replace with your actual directory path

    # Call the function to rename files in the directory
    rename_files_in_directory(dir_output)
