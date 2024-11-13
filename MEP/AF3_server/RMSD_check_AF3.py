import re

def parse_rmsd_data(file_path):
    rmsd_data = {}
    current_key = None

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('>'):
                #proteins = re.findall(r'\b\w+\b', line)
                proteins = line.split('_')[1: ] #dit moet even anders ik heb dat ergens in een andere python file well dat ik zoek naar de protein names
                # Create a unique sorted tuple of protein names to use as a key
                key = proteins
                current_key = key
                if current_key not in rmsd_data:
                    rmsd_data[current_key] = []
            else:
                # Extract RMSD value
                match = re.search(r'RMSD=([\d\.]+)', line)
                if match and current_key:
                    rmsd_value = float(match.group(1))
                    rmsd_data[current_key].append(rmsd_value)

    return rmsd_data

def save_rmsd_data(rmsd_data, output_file):
    with open(output_file, 'w') as f:
        f.write("Protein_Set\t" + "\t".join([f"RMSD_Score{i+1}" for i in range(max(len(v) for v in rmsd_data.values()))]) + "\tAverage_Score\n")
        for proteins, values in rmsd_data.items():
            average_score = sum(values) / len(values)
            f.write(f"{proteins}\t" + "\t".join(map(str, values)) + f"\t{average_score:.3f}\n")


# files + calling functions
file_path = '../AF3_server/Pymol_output_AF3check_RMSD_v3.txt'
output_file = 'rmsd_results_AF3.tsv'
rmsd_data = parse_rmsd_data(file_path)
save_rmsd_data(rmsd_data, output_file)
