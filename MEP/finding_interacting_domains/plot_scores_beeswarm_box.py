import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import pickle

# Load AF2 and AF3 score data from the uploaded TSV files
file_path_AF2 = 'scores_AF2_list2_withoutduplicates.tsv'
file_path_AF3 = 'scores_AF3_list2.tsv'

df_AF2 = pd.read_csv(file_path_AF2, sep='\t')
df_AF3 = pd.read_csv(file_path_AF3, sep='\t')

# Ensure protein names in AF3 start with a capital letter
df_AF3['protein1'] = df_AF3['protein1'].str.capitalize()
df_AF3['protein2'] = df_AF3['protein2'].str.capitalize()

# Standardize protein pair order in AF2 by sorting each pair alphabetically
df_AF2['protein_pair'] = df_AF2.apply(lambda row: tuple(sorted([row['protein1'], row['protein2']])), axis=1)
af2_pairs = set(df_AF2['protein_pair'])

# Standardize protein pair order in AF3 by sorting each pair alphabetically
df_AF3['protein_pair'] = df_AF3.apply(lambda row: tuple(sorted([row['protein1'], row['protein2']])), axis=1)

# Identify protein pairs present in AF3 but not in AF2
unique_to_af3_pairs = df_AF3[~df_AF3['protein_pair'].isin(af2_pairs)]
common_af3_pairs = df_AF3[df_AF3['protein_pair'].isin(af2_pairs)]

# Save the unique pairs data to a TSV file
output_path = 'unique_protein_pairs_AF3_not_in_AF2.tsv'
unique_to_af3_pairs.drop(columns=['protein_pair']).to_csv(output_path, sep='\t', index=False)
print(f"Saved unique protein pairs to {output_path}")

# Convert score columns to numeric, in case they were read as strings
score_columns_AF2 = ['iPTM', 'PTM']
score_columns_AF3 = ['iPTM', 'PTM', 'Fraction Disordered']
df_AF2[score_columns_AF2] = df_AF2[score_columns_AF2].apply(pd.to_numeric, errors='coerce')
df_AF3[score_columns_AF3] = df_AF3[score_columns_AF3].apply(pd.to_numeric, errors='coerce')
common_af3_pairs[score_columns_AF3] = common_af3_pairs[score_columns_AF3].apply(pd.to_numeric, errors='coerce')

# Function for simple beeswarm plotting
def simple_beeswarm2(y, nbins=None, width=1.):
    y = np.asarray(y)
    if len(y) == 0:
        return np.array([])  # Return empty if no data
    if nbins is None or nbins <= 0:
        nbins = max(1, np.ceil(len(y) / 6).astype(int))
    nn, ybins = np.histogram(y, bins=nbins)
    nmax = nn.max()
    x = np.zeros(len(y))
    ibs = []
    for ymin, ymax in zip(ybins[:-1], ybins[1:]):
        i = np.nonzero((y > ymin) * (y <= ymax))[0]
        ibs.append(i)
    dx = width / (nmax // 2) if nmax > 1 else width
    for i in ibs:
        yy = y[i]
        if len(i) > 1:
            j = len(i) % 2
            i = i[np.argsort(yy)]
            a = i[j::2]
            b = i[j + 1::2]
            x[a] = (0.5 + j / 3 + np.arange(len(b))) * dx
            x[b] = (0.5 + j / 3 + np.arange(len(b))) * -dx
    return x

# Function to create beeswarm plot with box and points
def plot_beeswarm_with_box_and_points(ax, df, metrics, title, palette="Set2"):
    boxplot_data = []
    count = 1
    colors = sns.color_palette(palette, len(metrics))  # Generate a color for each metric
    for i, metric in enumerate(metrics):
        y = df[metric].dropna()
        x = simple_beeswarm2(y, width=0.25)
        ax.plot(x + count, y, 'o', color=colors[i], alpha=0.6, label=metric)  # Use specific color
        boxplot_data.append(y)
        count += 1
    ax.boxplot(boxplot_data, widths=0.5, positions=np.arange(1, len(metrics) + 1))

    # Set x-tick labels with increased font size
    ax.set_xticks(np.arange(1, len(metrics) + 1))
    ax.set_xticklabels(metrics, fontsize=16, rotation=45, ha="right")  # Increase x-axis font size
    ax.set_title(title, fontsize=20)
    ax.set_xlabel('Metrics', fontsize=16)
    ax.set_ylabel('Values', fontsize=16)
    ax.tick_params(axis='y', labelsize=16)  # Increase y-axis font size
    ax.grid(True)

# Plotting
fig, axes = plt.subplots(1, 3, figsize=(30, 8))

# Metrics to plot for each
metrics_AF2 = ['iPTM', 'PTM']
metrics_AF3 = ['iPTM', 'PTM', 'Fraction Disordered']

# Plot for all AF3 pairs
plot_beeswarm_with_box_and_points(axes[0], df_AF3, metrics_AF3, 'All AF3 Scores', palette="Set2")

# Plot for common AF3 pairs (those that are also in AF2)
plot_beeswarm_with_box_and_points(axes[1], common_af3_pairs, metrics_AF3, 'AF3 Scores (Common with AF2)', palette="Set2")

# Plot for AF2 pairs
plot_beeswarm_with_box_and_points(axes[2], df_AF2, metrics_AF2, 'All AF2 Scores', palette="Set2")

# Set the same y-axis limits for all subplots from 0 to 1
for ax in axes:
    ax.set_ylim(0, 1)

# Add subplot labels (a), (b), and (c)
axes[0].text(-0.1, 1.05, "(a)", transform=axes[0].transAxes, size=20, weight="bold")
axes[1].text(-0.1, 1.05, "(b)", transform=axes[1].transAxes, size=20, weight="bold")
axes[2].text(-0.1, 1.05, "(c)", transform=axes[2].transAxes, size=20, weight="bold")

plt.tight_layout()
plt.show()
