import os

# Define the paths
fasta_dir = "AF_list2/fastapairs_list2"  # Replace with the path to your directory containing FASTA files
template_file = "bash_script_template.sh"  # Path to the uploaded template file
output_dir = "AF_list2/bash_scripts_list2"  # Directory where the generated scripts will be saved

# Read the template file
with open(template_file, "r") as file:
    template_content = file.read()

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Generate a Bash script for each FASTA file in the directory
for fasta_filename in os.listdir(fasta_dir):
    if fasta_filename.endswith(".fasta"):
        fasta_filepath = os.path.join(fasta_dir, fasta_filename)
        script_content = template_content.replace("name_fasta_file", fasta_filename)

        # Define the script filename based on the FASTA file name
        script_filename = os.path.join(output_dir, f"{os.path.splitext(fasta_filename)[0]}.sh")

        # Write the script content to the new file with Unix EOL
        with open(script_filename, "w", newline='\n') as script_file:
            script_file.write(script_content)

        print(f"Generated script: {script_filename}")

# Define the directory containing the generated bash scripts
bash_scripts_dir = output_dir # Replace with the path to your directory containing bash scripts
master_script_path = "AF_list2/submit_all_list2.sh"  # Path to the master script that will submit all individual scripts

#Create the master script
with open(master_script_path, "w", newline='\n') as master_script:
    master_script.write("#!/bin/sh\n#\n")

    # Iterate over each .sh file in the bash_scripts directory
    for bash_script in sorted(os.listdir(bash_scripts_dir)):
        if bash_script.endswith(".sh"):
            master_script.write(f"sbatch bash_scripts_list2/{bash_script}\n")

print(f"Master script generated: {master_script_path}")
