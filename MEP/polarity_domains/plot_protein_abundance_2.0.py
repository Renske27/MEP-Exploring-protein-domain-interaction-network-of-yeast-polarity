import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

# Input files
data_yeast = pd.read_csv('../data/fullyeast_data/count_relevant_domains_yeast_all.tsv', sep='\t')
data_abundance = pd.read_excel('C:/Users/rensk/OneDrive/Documenten/studie/afstuderen/data/protein_abundance_kulak_2014/41592_2014_BFnmeth2834_MOESM227_ESM.xlsx')
data_combined = pd.read_csv('../data/combined_set/count_domains_proteins_combinedset.tsv', sep='\t')

# This function searches in the dataframe df for the domain_accession and gives the proteins that have this domain
def search_domain_in_dataframe(df, domain_accession):
    row_values = df[df['Domain Accession'] == domain_accession]['Accession proteins'].values
    if len(row_values) > 0:
        return row_values[0]
    else:
        print(f"Accession {domain_accession} not found in {df} data")
        return ""

# This function gets the protein abundance from the dataframe
def protein_abundance(df_abundance, proteins_accession_str):
    df_abundance_proteins = pd.DataFrame(columns=df_abundance.columns)
    proteins_accession = ast.literal_eval(proteins_accession_str)
    # Remove duplicates by converting to set and back to list
    proteins_accession = list(set(proteins_accession))

    for item in proteins_accession:
        if df_abundance['Majority protein IDs'].isin([item]).any():
            row_to_append = df_abundance[df_abundance['Majority protein IDs'] == item]
            df_abundance_proteins = df_abundance_proteins.append(row_to_append, ignore_index=True)
    return df_abundance_proteins

# Function to plot protein abundance
def plot_protein_abundance(domain_accession, domain_name):
    proteins = search_domain_in_dataframe(data_yeast, domain_accession)
    protein_abundance_data = protein_abundance(data_abundance, proteins)
    proteins_combined_set = search_domain_in_dataframe(data_combined, domain_accession)

    # Filter out rows with NaN values in 'Gene names' and 'Majority protein IDs'
    protein_abundance_data = protein_abundance_data.dropna(subset=['Gene names'])

    # Sort data by copy number
    df_sorted = protein_abundance_data.sort_values(by="Copy number", ascending=False)

    # Create bar plot
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(df_sorted['Gene names'], df_sorted['Copy number'], color='cornflowerblue', label='Other Proteins')

    # Add labels
    for i, bar in enumerate(bars):
        yval = bar.get_height()
        if df_sorted['Majority protein IDs'].iloc[i] in ast.literal_eval(proteins_combined_set):
            bar.set_color('salmon')

    # Manually add a custom legend entry for the red bars
    red_bar = plt.Line2D([0], [0], color='salmon', lw=4, label='Proteins in Combined Set')
    gray_bar = plt.Line2D([0], [0], color='cornflowerblue', lw=4, label='Other Proteins')
    ax.legend(handles=[gray_bar, red_bar], fontsize=18)

    # Set labels and title with increased font sizes
    ax.set_xlabel('Proteins', fontsize=18)
    ax.set_ylabel('Copy number', fontsize=18)
    ax.set_title(f'Distribution of abundance of proteins with {domain_name} domain', fontsize=28)

    # Increase tick label font sizes
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=18)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=90)

    # Adjust layout for better fit
    plt.tight_layout()

    # Save the figure
    title = domain_name.replace(' ', '_')
    output_file = f"plot_protein_abundance_{title}.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')

    # Close the figure
    plt.close(fig)

# Plot for SH3 domain
domain_accesion_SH3 = "IPR001452"
plot_protein_abundance(domain_accesion_SH3, 'SH3')

# Plot for PH domain
domain_accesion_PH = "IPR001849"
plot_protein_abundance(domain_accesion_PH, 'PH')
