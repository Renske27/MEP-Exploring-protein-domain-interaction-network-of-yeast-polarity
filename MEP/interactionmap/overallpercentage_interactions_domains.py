import pandas as pd

# Load the CSV file
file_path = "../data/list2_data/interactionmap_data/domain_contacts_plDDT50_noscorethres.csv"
df = pd.read_csv(file_path, sep='\t')

# Initialize counts for overall interactions
total_within_domain_count = 0
total_outside_domain_count = 0
total_mixed_domain_count = 0
total_interactions = 0

# Iterate over each interaction and categorize them
for _, row in df.iterrows():
    domain1 = row['Domain1_Accession']
    domain2 = row['Domain2_Accession']
    count = row['Count']

    # Categorize interactions
    if domain1 != 'None' and domain2 != 'None':
        total_within_domain_count += count
    elif domain1 == 'None' and domain2 == 'None':
        total_outside_domain_count += count
    else:
        total_mixed_domain_count += count

    # Add to the total number of interactions
    total_interactions += count

# Calculate percentages
if total_interactions > 0:
    overall_within_domain_percentage = (total_within_domain_count / total_interactions) * 100
    overall_outside_domain_percentage = (total_outside_domain_count / total_interactions) * 100
    overall_mixed_domain_percentage = (total_mixed_domain_count / total_interactions) * 100
else:
    overall_within_domain_percentage = 0
    overall_outside_domain_percentage = 0
    overall_mixed_domain_percentage = 0

# Print the overall percentages
print(f"Total Interactions: {total_interactions}")
print(f"Interactions Within Domains (%): {overall_within_domain_percentage:.2f}%")
print(f"Interactions Outside Domains (%): {overall_outside_domain_percentage:.2f}%")
print(f"Mixed Interactions (%): {overall_mixed_domain_percentage:.2f}%")

# Save the results to a CSV file
output_file_path = 'overall_interaction_percentages_AF3plDDT50_nosccorethres.csv'
results = {
    'Total Interactions': [total_interactions],
    'Interactions Within Domains (%)': [overall_within_domain_percentage],
    'Interactions Outside Domains (%)': [overall_outside_domain_percentage],
    'Mixed Interactions (%)': [overall_mixed_domain_percentage]
}
results_df = pd.DataFrame(results)
results_df.to_csv(output_file_path, index=False)

print(f"Results saved to {output_file_path}")
