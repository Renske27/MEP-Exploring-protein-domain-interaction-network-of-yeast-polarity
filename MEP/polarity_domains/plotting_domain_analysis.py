# venn diagram of unique domains
# scatter plots ratio domain occurs in protein set vs ratio domain occurs in full yeast proteome


#%%
import pandas as pd
from matplotlib import pyplot as plt
from venn import venn
from matplotlib_venn import venn2, venn3, venn3_circles
import numpy as np
from Data_to_file import *
import plotly.express as px

# Function to read tsv files
def read_tsv(file_path):
    """Function to read a TSV file into a pandas DataFrame."""
    return pd.read_csv(file_path, sep='\t')

# Load domain data of all possible sets
allGOterms = read_tsv('../data/allGoterm_data/count_domains_proteins_allGOterms.tsv')
Daalman_data = read_tsv('../data/Daalman_data/count_domains_Daalman_proteinlist.tsv')
strCdc42bem1cdc24 = read_tsv('../data/fullstrCdc42Bem1Cdc24_data/count_domains_proteins_fullstrCdc42Bem1Cdc24.tsv')
Goterm = read_tsv('../data/Goterm_data/count_domains_proteins_GOterm.tsv')
list2 = read_tsv('../data/list2_data/count_domains_protein_list2.tsv')
physstrcdc42bem1cdc24 = read_tsv('../data/physstrCdc42Bem1Cdc24_data/count_domains_proteins_physstrCdc42Bem1Cdc24.tsv')
strfullcdc42 = read_tsv('../data/fullstr_Cdc42_settings/count_domains_proteins_fullstrCdc42.tsv')
strphyscdc42 = read_tsv('../data/physstr_Cdc42_settings/count_domains_proteins_physstrCdc42.tsv')
combinedset = read_tsv('../data/combined_set/count_domains_proteins_combinedset.tsv')
fullyeast= read_tsv("../data/fullyeast_data/count_relevant_domains_yeast_all.tsv")

# Extract the unique domain sets from the data
protein_sets = {
    "Set20": set(list2["Domain Accession"]),
    "Daalman": set(Daalman_data["Domain Accession"]),
    "GO:0007163": set(Goterm["Domain Accession"]),
    "GO:polarity": set(allGOterms["Domain Accession"]),
    "String full Cdc42": set(strfullcdc42["Domain Accession"]),
    "String physical Cdc42": set(strphyscdc42["Domain Accession"]),
    "String full Cdc42 Bem1 Cdc24": set(strCdc42bem1cdc24["Domain Accession"]),
    "String physical Cdc42 Bem1 Cdc24": set(physstrcdc42bem1cdc24["Domain Accession"]),
    "Combined set": set(combinedset["Domain Accession"]),
    "Full yeast proteome": set(fullyeast["Domain Accession"])
}

# Create a Venn diagram for the first three sets (you can create additional Venn diagrams for other combinations)
set1 = protein_sets["Set20"]
set2 = protein_sets["Combined set"]
set3 = protein_sets["Full yeast proteome"]

venn_data = [set1, set2, set3]
labels = ["Set20", "Combined set", "Full yeast"]

# Create the Venn diagram
plt.figure(figsize=(10, 7))
venn3([set1, set2, set3], set_labels=labels)

# Save the Venn diagram as an image
plt.title("Venn Diagram of unique domains")
plt.savefig('venn_domains-set_combined_yeast.png')
plt.show()

# Create a Venn diagram for the first three sets (you can create additional Venn diagrams for other combinations)
set1 = protein_sets["Set20"]
set2 = protein_sets["GO:polarity"]
set3 = protein_sets["Daalman"]

venn_data = [set1, set2, set3]
labels = ["Set20", "GO:polarity", "Daalman"]

# Create the Venn diagram
plt.figure(figsize=(10, 7))
venn3([set1, set2, set3], set_labels=labels)

# Save the Venn diagram as an image
plt.title("Venn Diagram of unique domains")
plt.savefig('venn_domains-set_GO_daalman.png')
plt.show()

# Create a Venn diagram for the first three sets (you can create additional Venn diagrams for other combinations)
set1 = protein_sets["String physical Cdc42 Bem1 Cdc24"]
set2 = protein_sets["GO:polarity"]
set3 = protein_sets["String full Cdc42 Bem1 Cdc24"]

venn_data = [set1, set2, set3]
labels = ["String physical Cdc42 Bem1 Cdc24", "GO:polarity", "String full Cdc42 Bem1 Cdc24"]

# Create the Venn diagram
plt.figure(figsize=(10, 7))
venn3([set1, set2, set3], set_labels=labels)

# Save the Venn diagram as an image
plt.title("Venn Diagram of unique domains")
plt.savefig('venn_domains-strphysall_GO_strfullall.png')
plt.show()

# Create a Venn diagram for the first three sets (you can create additional Venn diagrams for other combinations)
set1 = protein_sets["String physical Cdc42"]
set2 = protein_sets["String full Cdc42 Bem1 Cdc24"]
set3 = protein_sets["String full Cdc42"]

venn_data = [set1, set2, set3]
labels = ["String physical Cdc42", "String full Cdc42 Bem1 Cdc24", "String full Cdc42"]

# Create the Venn diagram
plt.figure(figsize=(10, 7))
venn3([set1, set2, set3], set_labels=labels)

# Save the Venn diagram as an image
plt.title("Venn Diagram of unique domains")
plt.savefig('venn_domains-strphyscdc42_strfullall_strfullcdc42.png')
plt.show()

# Create a Venn diagram for the first three sets (you can create additional Venn diagrams for other combinations)
set1 = protein_sets["String physical Cdc42 Bem1 Cdc24"]
set2 = protein_sets["Daalman"]
set3 = protein_sets["String full Cdc42 Bem1 Cdc24"]

venn_data = [set1, set2, set3]
labels = ["String physical Cdc42 Bem1 Cdc24", "Daalman", "String full Cdc42 Bem1 Cdc24"]

# Create the Venn diagram
plt.figure(figsize=(10, 7))
venn3([set1, set2, set3], set_labels=labels)

# Save the Venn diagram as an image
plt.title("Venn Diagram of unique domains")
plt.savefig('venn_domains-strphysall_Daalman_strfullall.png')
plt.show()

# Create a Venn diagram for the first three sets (you can create additional Venn diagrams for other combinations)
set1 = protein_sets["GO:polarity"]
set2 = protein_sets["Daalman"]
set3 = protein_sets["String full Cdc42 Bem1 Cdc24"]

venn_data = [set1, set2, set3]
labels = ["GO:polarity", "Daalman", "String full Cdc42 Bem1 Cdc24"]

# Create the Venn diagram
plt.figure(figsize=(10, 7))
venn3([set1, set2, set3], set_labels=labels)

# Save the Venn diagram as an image
plt.title("Venn Diagram of unique domains")
plt.savefig('venn_domains-GOall_Daalman_strfullall.png')
plt.show()

# Create a Venn diagram for the first three sets (you can create additional Venn diagrams for other combinations)
set1 = protein_sets["GO:polarity"]
set2 = protein_sets["Daalman"]
set3 = protein_sets["String full Cdc42"]

venn_data = [set1, set2, set3]
labels = ["GO:polarity", "Daalman", "String full Cdc42"]

# Create the Venn diagram
plt.figure(figsize=(10, 7))
venn3([set1, set2, set3], set_labels=labels)

# Save the Venn diagram as an image
plt.title("Venn Diagram of unique domains")
plt.savefig('venn_domains-GOall_Daalman_strfullcdc42.png')
plt.show()

# Create a Venn diagram for the first three sets (you can create additional Venn diagrams for other combinations)
set1 = protein_sets["GO:polarity"]
set2 = protein_sets["GO:0007163"]


venn_data = [set1, set2]
labels = ["GO:polarity", "GO:0007163"]

# Create the Venn diagram
plt.figure(figsize=(10, 7))
venn2([set1, set2], set_labels=labels)

# Save the Venn diagram as an image
plt.title("Venn Diagram of unique domains")
plt.savefig('venn_domains-GOall.png')
#plt.show()

# Create a Venn diagram for the first three sets (you can create additional Venn diagrams for other combinations)
set1 = protein_sets["GO:polarity"]
set2 = protein_sets["Daalman"]
set3 = protein_sets["String physical Cdc42"]

venn_data = [set1, set2, set3]
labels = ["GO:polarity", "Daalman", "String physical Cdc42"]

# Create the Venn diagram
plt.figure(figsize=(10, 7))
venn3([set1, set2, set3], set_labels=labels)

# Save the Venn diagram as an image
plt.title("Venn Diagram of unique domains")
plt.savefig('venn_domains-GOall_Daalman_strphyscdc42.png')
#plt.show()


#%% Scatterplots:
import random
# Function to create a scatter plot
def create_scatter_plot(data, title):
    # Sort data by 'N_d_yeast/N_p_yeast'
    data = data.sort_values(by=['N_d_yeast/N_p_yeast'])

    # Extract x and y values
    x_values = data['N_d_yeast/N_p_yeast']
    y_values = data['N_d_list/N_p_list']
    labels = data["Domain name"]

    # # Plotting with labels
    # fig1, ax1 = plt.subplots()
    # ax1.scatter(x_values, y_values, s=50, alpha=0.5)
    #
    # # Add labels to each data point
    # for i, label in enumerate(labels):
    #     ax1.text(x_values.iloc[i], y_values.iloc[i], label, fontsize=8)
    #
    # # Add diagonal line x=y
    # x_values_2 = np.linspace(0, max(x_values.max(), y_values.max()), 50)
    # ax1.plot(x_values_2, x_values_2, label='x=y', linestyle='--')
    #
    # # Set axis labels, title, and legend
    # ax1.set_xlabel("Domain occurrence in yeast/Total number of proteins yeast")
    # ax1.set_ylabel("Domain occurrence in set/Number of proteins in set")
    # ax1.set_title(f"Scatterplot domains within {title}")
    # ax1.legend()
    # ax1.set_xlim(0, 0.025)
    #
    # # Save the figure
    # output_file = output_file_frontextension('plot_ratios', f"{title.replace(' ', '_')}.tsv", 'png')
    # plt.savefig(output_file, dpi=300, bbox_inches='tight')
    # plt.close(fig1)


    # interactive plotting
    fig = px.scatter(data, x='N_d_yeast/N_p_yeast', y='N_d_list/N_p_list',
                       title=f"Scatterplot {title}", #text='Domain name',
                     labels={'N_d_yeast/N_p_yeast': 'N_d_yeast/N_p_yeast', 'N_d_list/N_p_list': 'N_d_list/N_p_list'},
                     opacity=0.7)
    fig.update_traces(marker=dict(size=8), selector=dict(mode='markers'))
    fig.update_layout(showlegend=True)

    # Add diagonal line x=y
    fig.add_shape(type="line",
                  x0=0, y0=0, x1=max(x_values.max(), y_values.max()), y1=max(x_values.max(), y_values.max()),
                  line=dict(dash="dash"))

    # Add labels with random jitter for figure in thesis (without with text='Domain name' to github for people to look into and hover over it.
    for i in range(len(labels)):
        jitter_x = random.uniform(-0.0005, 0.0005)
        jitter_y = random.uniform(-0.0005, 0.0005)
        fig.add_annotation(
            x=x_values.iloc[i] + jitter_x,
            y=y_values.iloc[i] + jitter_y,
            text=labels.iloc[i],
            showarrow=False,
            font=dict(size=16)
        )

    # Fix the axes range
    fig.update_xaxes(range=[0, 0.025])
    #fig.update_yaxes(range=[0, x_values.max()])

    # Save the figure
    output_file = output_file_frontextension('plot_int_ratios', f"{title.replace(' ', '_')}.tsv", 'html')
    fig.write_html(output_file)


# Create scatter plots for each dataset
datasets = {
    "GO polarity": allGOterms,
    "Daalman_data": Daalman_data,
    "String full Cdc42 Bem1 Cdc24": strCdc42bem1cdc24,
    "GO 0007163": Goterm,
    "Set 20": list2,
    "String physical Cdc42 Bem1 Cdc24": physstrcdc42bem1cdc24,
    "String full Cdc42": strfullcdc42,
    "String physical Cdc42": strphyscdc42,
    "Combined set": combinedset
}


# Generate scatter plots for each dataset
for title, data in datasets.items():
    create_scatter_plot(data, title)