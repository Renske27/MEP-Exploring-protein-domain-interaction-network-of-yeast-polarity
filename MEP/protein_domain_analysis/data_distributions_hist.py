import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Function to read JSON files
def read_json(file_path):
    """Function to read a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

# Load domain data of all possible sets
datasets = {
    "GO:all_polarity": read_json('../data/allGoterm_data/domains_proteins_allGOterms.json'),
    "Daalman": read_json('../data/Daalman_data/domains_Daalman_proteinlist.json'),
    "String_Cdc42Bem1Cdc24": read_json('../data/fullstrCdc42Bem1Cdc24_data/domains_proteins_fullstrCdc42Bem1Cdc24.json'),
    "Set20": read_json('../data/list2_data/domains_protein_list2_with_pI.json'),
    "Fullyeast": read_json("../data/fullyeast_data/relevant_domains_yeast_all.json")
}

# Initialize lists to store all datasets together
combined_data = []


# Function to extract information and calculate coverage considering overlaps
def extract_protein_info(protein, dataset_name):
    length = int(protein['length'])
    mass = int(protein['mass']) / 1000  # Convert to kDa for easier visualization
    pI_protein = protein.get('protein_pI', None)  # Safely access 'protein_pI'
    domain_lengths = [int(domain['domain_end']) - int(domain['domain_start']) + 1 for domain in
                      protein.get('domains', [])]
    domain_pI = [domain.get('domain_pI', None) for domain in protein.get('domains', [])]  # Safely access 'domain_pI'

    # Calculate non-overlapping domain coverage
    domain_positions = []
    for domain in protein.get('domains', []):
        domain_start = int(domain['domain_start'])
        domain_end = int(domain['domain_end'])
        domain_positions.append((domain_start, domain_end))
    domain_positions = sorted(domain_positions, key=lambda x: x[0])  # Sort by start position

    covered_positions = []
    for start, end in domain_positions:
        if not covered_positions or start > covered_positions[-1][1]:
            covered_positions.append((start, end))
        else:
            covered_positions[-1] = (covered_positions[-1][0], max(covered_positions[-1][1], end))

    total_coverage = sum(end - start + 1 for start, end in covered_positions)
    coverage_percentage = total_coverage / length * 100 if length else 0

    # Add a separate row for each domain length
    for domain_length, domain_pI_value in zip(domain_lengths, domain_pI):
        combined_data.append({
            'Protein Length': length,
            'Protein pI': pI_protein,
            'Domain Length': domain_length,
            'Domain pI': domain_pI_value,
            'Number of Domains': len(domain_lengths),
            'Domain Coverage (%)': coverage_percentage,
            'Dataset': dataset_name
        })


# Process each dataset
for name, data in datasets.items():
    for protein in data:
        extract_protein_info(protein, name)

# Create a DataFrame for combined data
df_combined = pd.DataFrame(combined_data)

# Plotting KDE plots with metrics on x-axis and density on y-axis
metrics = ['Protein Length', 'Protein pI', 'Domain Length', 'Domain pI', 'Number of Domains', 'Domain Coverage (%)']
fig, axes = plt.subplots(3, 2, figsize=(15, 15))

# Flatten axes for easier iteration
axes = axes.flatten()

# Create KDE plots using sns.kdeplot
for i, metric in enumerate(metrics):
    sns.kdeplot(data=df_combined, x=metric, hue='Dataset', ax=axes[i], palette='muted', fill=False, common_norm=False)
    axes[i].set_xlabel(metric, fontsize=16)  # Set the x-label with increased font size
    axes[i].set_ylabel('Density', fontsize=16)  # Set the y-label with increased font size

    # Manually set font size for x and y axis ticks
    axes[i].tick_params(axis='x', labelsize=14)
    axes[i].tick_params(axis='y', labelsize=14)

    # Increase font size of the legend
    legend = axes[i].get_legend()
    if legend:
        legend.set_title("Dataset")
        plt.setp(legend.get_texts(), fontsize=14)
        plt.setp(legend.get_title(), fontsize=14)

    # Ensure that the x-axis limits and ticks are appropriate
    x_min, x_max = df_combined[metric].min(), df_combined[metric].max()
    axes[i].set_xlim(x_min, x_max)

# Add a), b), c) labels under each subplot
labels = ['a)', 'b)', 'c)', 'd)', 'e)', 'f)']
for i, ax in enumerate(axes):
    ax.text(-0.1, 1.1, labels[i], transform=ax.transAxes,
            fontsize=16, va='top', ha='left')

# Adjustments and layout settings
plt.tight_layout()

# Save the figure to a file
output_file = 'protein_domain_data_distributions_2.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')

plt.show()
