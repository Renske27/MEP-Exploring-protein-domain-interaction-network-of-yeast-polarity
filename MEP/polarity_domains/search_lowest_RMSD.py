import pandas as pd

# Load the Excel file
file_path = 'C:/Users/rensk/OneDrive/Documenten/studie/afstuderen/average_domain_script/RMSD_PH_models_RMSD_after_refinement2.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Calculate the sum of each numeric column
column_sums = df.select_dtypes(include='number').sum()

# Add the sums as the last row
df.loc['Sum'] = df.select_dtypes(include='number').sum()

# Save the modified DataFrame back to the Excel file
with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=True)
    worksheet = writer.sheets['Sheet1']
    worksheet.set_column(0, len(df.columns), 12)  # Adjust column width for better readability
    worksheet.hide_gridlines()  # Hide gridlines for a cleaner look

# Print the column name with the lowest sum
lowest_sum_column = column_sums.idxmin()
print(f"Column with the lowest sum: {lowest_sum_column}")
