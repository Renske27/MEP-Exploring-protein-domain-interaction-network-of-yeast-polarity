
from pymol import cmd

cmd.delete('all')  # Delete all loaded structures from PyMOL

# Load the CIF file
file = "C:/Users/rensk/OneDrive/Documenten/studie/afstuderen/data/alphafold3/unpacked_unique/bem1_cdc24/fold_fold_23_cdc24_bem1_model_0.cif"
cmd.load(file, format='cif')

# Color chains A and B
cmd.color('lightpink', 'chain A')
cmd.color('palecyan', 'chain B')

# Color specific domains in chain A
cmd.color('lightmagenta', 'resi 135-246 and chain A')  # Calponin homology domain
cmd.color('pink', 'resi 278-454 and chain A')  # DH
cmd.color('violet', 'resi 478-670 and chain A')  # PH
cmd.color('violetpurple', 'resi 761-854 and chain A')  # PB1

# # Color specific domains in chain A
# cmd.color('tv_blue', 'resi 135-246 and chain A')  # Calponin homology domain
# cmd.color('slate', 'resi 278-454 and chain A')  # DH
# cmd.color('deepblue', 'resi 478-670 and chain A')  # PH
# cmd.color('density', 'resi 761-854 and chain A')  # PB1

# Color specific domains in chain B
cmd.color('aquamarine', 'resi 72-132 and chain B')  # SH3
cmd.color('aquamarine', 'resi 155-217 and chain B')  # SH3
cmd.color('greencyan', 'resi 278-404 and chain B')  # PX
cmd.color('deepteal', 'resi 478-551 and chain B')  # PB1

#List of residue numbers interacting in chain A (no plDDt threshold or other score threshold)
residue_numbers_A = [
    66, 69, 69, 136, 136, 138, 138, 187, 188, 188, 190, 191, 197, 200, 200,
    219, 304, 308, 315, 316, 316, 316, 316, 316, 317, 317, 319, 319, 320, 320,
    320, 367, 367, 368, 368, 371, 371, 372, 375, 375, 379, 450, 454, 457, 457,
    457, 461, 461, 480, 800, 803, 804, 808, 815, 817, 817, 818, 820, 820, 821,
    822, 824, 824, 824, 824, 825, 826, 826, 826, 827, 827, 827, 830, 832, 832,
    833, 833, 836, 839, 840
]

# # # List of residue numbers interacting in chain A with plDDT>70 threshold
# residue_numbers_A = [815, 817, 818, 820, 821, 822, 824, 825, 826, 827, 830, 832, 833, 836, 839, 840]

# Remove duplicates and sort the residue numbers
unique_residues_A = sorted(set(residue_numbers_A))

# Select and color the residues in chain A
for resi in unique_residues_A:
    cmd.select(f'residue_A_{resi}', f'chain A and resi {resi}')
    cmd.color('firebrick', f'residue_A_{resi}')

# List of residue numbers to be colored in red in chain B
residue_numbers_B = [
    18, 19, 20, 21, 152, 153, 154, 154, 159, 159, 159, 178, 179, 180, 183, 183,
    196, 196, 196, 197, 198, 198, 198, 198, 199, 201, 201, 204, 215, 217, 217,
    217, 219, 220, 249, 250, 253, 256, 322, 338, 340, 346, 346, 353, 354, 356,
    357, 359, 359, 359, 359, 360, 360, 480, 480, 480, 482, 482, 482, 484, 487,
    488, 488, 488, 489, 489, 489, 489, 490, 490, 491, 491, 491, 493, 493, 506,
    510, 510, 510, 545
]

# # List of residue numbers interacting in chain B with plDDT>70 threshold
# residue_numbers_B = [480, 482, 484, 487, 488, 489, 490, 491, 493, 506, 510, 512, 545]


# Remove duplicates and sort the residue numbers
unique_residues_B = sorted(set(residue_numbers_B))

# Select and color the residues in chain B
for resi in unique_residues_B:
    cmd.select(f'residue_B_{resi}', f'chain B and resi {resi}')
    cmd.color('firebrick', f'residue_B_{resi}')

# # Create a legend using pseudoatoms and labels
# def create_legend():
#     # Set starting position for legend outside the 3D structure
#     x_pos = 80
#     x_add = -200
#     y_pos = 0
#     spacing = 10  # Space between legend items
#     cmd.pseudoatom("legendA", pos=[x_pos, y_pos, 0], label="Cdc24 (lightpink)")
#     cmd.set("label_color", "lightpink", "legendA")
#     cmd.pseudoatom("legendB", pos=[x_pos + x_add, y_pos, 0], label="Bem1 (palecyan)")
#     cmd.set("label_color", "palecyan", "legendB")
#
#     # Add domain color labels for chain A
#     cmd.pseudoatom("legendA_calponin", pos=[x_pos, y_pos - 2 * spacing, 0], label="CH domain (lightmagenta)")
#     cmd.set("label_color", "lightmagenta", "legendA_calponin")
#     cmd.pseudoatom("legendA_DH", pos=[x_pos, y_pos - 3 * spacing, 0], label="DH Domain (pink)")
#     cmd.set("label_color", "pink", "legendA_DH")
#     cmd.pseudoatom("legendA_PH", pos=[x_pos, y_pos - 4 * spacing, 0], label="PH Domain (violet)")
#     cmd.set("label_color", "violet", "legendA_PH")
#     cmd.pseudoatom("legendA_PB1", pos=[x_pos, y_pos - 5 * spacing, 0], label="PB1 Domain (violetpurple)")
#     cmd.set("label_color", "violetpurple", "legendA_PB1")
#
#     # Add domain color labels for chain B
#     cmd.pseudoatom("legendB_SH3", pos=[x_pos + x_add, y_pos - spacing, 0], label="SH3 Domain (aquamarine)")
#     cmd.set("label_color", "aquamarine", "legendB_SH3")
#     cmd.pseudoatom("legendB_PX", pos=[x_pos + x_add, y_pos - 2 * spacing, 0], label="PX Domain (greencyan)")
#     cmd.set("label_color", "teal", "legendB_PX")
#     cmd.pseudoatom("legendB_PB1", pos=[x_pos + x_add , y_pos - 3 * spacing, 0], label="PB1 Domain (deepteal)")
#     cmd.set("label_color", "deepteal", "legendB_PB1")
#
    # Color for interacting residues
    cmd.pseudoatom("legend_residues", pos=[x_pos + x_add, y_pos - 4 * spacing, 0], label="Interacting Residues (firebrick)")
    cmd.set("label_color", "firebrick", "legend_residues")
#
# # Call the function to create the legend
# create_legend()

cmd.zoom()