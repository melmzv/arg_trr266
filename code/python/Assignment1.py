import pandas as pd
import numpy as np 


'''
Step 1
'''
# Load the data from Worldscope files into pandas DataFrames
static_data = pd.read_csv('/Users/melissam/Documents/Uni🏅🩷/SS 24🥇/708014 Accounting Reading Group/Assignment I/wscp_static.txt', delimiter='\t') # use '\t' due to tab-separation in the static file
panel_data = pd.read_excel('/Users/melissam/Documents/Uni🏅🩷/SS 24🥇/708014 Accounting Reading Group/Assignment I/wscp_panel.xlsx')
# Normalize column names to avoid issues caused by variation in column naming conventions
static_data.columns = static_data.columns.str.strip().str.lower().str.replace(' ', '_')
panel_data.columns = panel_data.columns.str.strip().str.lower().str.replace(' ', '_')

# Merge data on 'isin' to include country information in panel_data
merged_data = panel_data.merge(static_data[['isin', 'country']], on='isin', how='left')
# Print the merged data to check. Now we have added a column on countries in panel data
print("Step 1: Merged data sample on 'isin' from static and panel data:\n", merged_data.head(11))
print()  # add this to get a blank line for better readability
# To understand how many rows there are in the merged data
num_rows1 = len(merged_data)
print("Number of rows in merged data sample on 'isin' from static and panel data:", num_rows1)
print()
print()


'''
Step 2
'''
# Filter the merged data for US firms and years 1996-2015
us_firms = merged_data[merged_data['country'] == 'UNITED STATES'] # create a new DataFrame that contains only US firms
filtered_data = us_firms[(us_firms['year_'] >= 1996) & (us_firms['year_'] <= 2015)].copy() # further filter the us_firms DataFrame to keep the task's required year range
# Print the filtered data to check
print("Step 2: Filtered data sample on US firms and years 1996-2015:\n", filtered_data.head(22))
print()
# To understand how many rows were dropped out
num_rows2 = len(filtered_data)
print("Number of rows in filtered data sample on US firms and years 1996-2015:", num_rows2)
print()
print()


'''
Step 3
'''
# Identify Year 0 to Year 6 for each firm within the filtered data
filtered_data['year_0'] = filtered_data.groupby('isin')['year_'].transform('min') # this column will hold the according “Year 0” for each firm
filtered_data['relative_year'] = filtered_data['year_'] - filtered_data['year_0'] # this column now indicates how many years have passed since the firm’s “Year 0”
filtered_data = filtered_data[filtered_data['relative_year'] <= 6] # filter the data to include only the first seven years (Year 0 to Year 6) for each firm
# Print the filtered data to check if it's empty or has data
print("Step 3: Filtered data sample after identifying the Year 0 and relative years:\n", filtered_data.head(22))
print()
# To understand how many rows were dropped out
num_rows3 = len(filtered_data)
print("Number of rows in filtered data sample after identifying the Year 0 and relative years:", num_rows3)
print()
print()


'''
Step 4
'''
# Calculate P/B Ratio for each firm in Year 0

year_0_data = filtered_data[filtered_data['relative_year'] == 0].copy() # create a copy of filtered_data DataFrame to contain only data for Year 0
print("Step 4: Year 0 data:\n", year_0_data)
print()

year_0_data['bve'] = year_0_data['bve'].replace([0, np.inf, -np.inf], np.nan) # replace zero and very small BVE values with NaN
# To verify: display rows where 'bve' is NaN
nan_bve_rows = year_0_data[year_0_data['bve'].isna()]
print("Rows where 'bve' has been replaced with NaN:\n", nan_bve_rows)
num_nan_bve_rows = len(nan_bve_rows)
print("Number of rows where 'bve' has been replaced with NaN:", num_nan_bve_rows)
print()

# Use P/B Ratio formula to calculate it for each firm in Year 0
year_0_data['p/b'] = year_0_data['mve'] / year_0_data['bve']

# Before removing NaN P/B ratios
num_rows_before = len(year_0_data)
# Remove rows with NaN P/B ratios
year_0_data = year_0_data.dropna(subset=['p/b'])
# After removing NaN P/B ratios
num_rows_after = len(year_0_data) 

# Calculate the number of dropped observations
num_dropped = num_rows_before - num_rows_after
print("Number of observations dropped due to NaN P/B ratios:", num_dropped) # checked: the number of dropped observations is equal to number of dropped BVE observations
print("Number of rows in Year 0 data after removing NaN P/B ratios:", num_rows_after)
print("Year 0 data after calculating P/B ratio and dropping NaN values:\n", year_0_data) # the DataFrame now contains new column p/b ratio
print()
print()


'''
Step 5
'''
# Form P/B groups

# Sort firms based on their P/B ratios for Year 0 in descending order
num_groups = 20  # define the number of groups
year_0_data = year_0_data.sort_values('p/b', ascending=False).reset_index(drop=True) # sort the year_0_data DataFrame in descending order based on the P/B ratios
print("Step 5: Year 0 data sorted in descending order based on the P/B ratios:\n", year_0_data) # check the correct order
print()

# Assign the groups so that the highest P/B ratios are in group 1 and lowest in group 20
year_0_data['p/b_group'] = pd.qcut(year_0_data.index, num_groups, labels=range(1, num_groups + 1))
print("Year 0 data updated with P/B groups:\n",year_0_data) # checked: p/b ratios grouping aligns with previous output

# Count the number of firms in each P/B group before merging
pb_group_counts_pre_merge = year_0_data.groupby('p/b_group', observed=True)['isin'].nunique()
print("Number of firms assigned to each P/B group before merging:\n", pb_group_counts_pre_merge)
print()

# Calculate median P/B value for each group
median_pb_values = year_0_data.groupby('p/b_group', observed=True)['p/b'].median()
# Display the median P/B values
print("Median P/B values for each group:\n", median_pb_values)
print()

# Merge the P/B groups back to the filtered data for Year 0
filtered_data = filtered_data.merge(year_0_data[['isin', 'p/b_group']], on='isin', how='left')
# Fill missing P/B groups for years other than Year 0 with the same group as Year 0
filtered_data['p/b_group'] = filtered_data.groupby('isin')['p/b_group'].ffill()

# Display the combined filtered data after merging P/B groups
print("Filtered data after merging P/B groups:\n", filtered_data.head(22)) # the DataFrame now contains new column p/b_group
# Count the number of firms in each P/B group after merging
pb_group_counts_post_merge = filtered_data.groupby('p/b_group', observed=True)['isin'].nunique()
print("Number of firms assigned to each P/B group after merging:\n", pb_group_counts_post_merge) # checked: same number as pre merging
# Calculate the number of rows in the merged filtered data sample
num_rows_merged_filtered = len(filtered_data)
print("Number of rows in the merged filtered data sample:", num_rows_merged_filtered) # checked: same number as pre merging
print()


'''
Step 6
'''
# Calculate residual income for each P/B group for Years 0 to 6, deflated by the book value of equity at the end of the year before Year 0 (= beginning of year 0)

cost_of_equity = 0.08  # assumption for cost of equity capital

# Create a copy of the merged data from Step 1 to preserve all years of observations
us_full_data = merged_data[merged_data['country'] == 'UNITED STATES'].copy()
print("Step 6: Merged data (Step 1) filtered to US only, all years preserved:\n", us_full_data.head(22))
print()

# Identify Year 0 for each firm, ensuring Year 0 is between 1996 and 2015
us_full_data['year_0'] = us_full_data.groupby('isin')['year_'].transform(lambda x: x[(x >= 1996) & (x <= 2015)].min())
us_full_data = us_full_data[us_full_data['year_0'].notna()]  # remove rows where year_0 is NaN
# Calculate the relative year and year_minus_1
us_full_data['relative_year'] = us_full_data['year_'] - us_full_data['year_0']
us_full_data['year_minus_1'] = us_full_data['year_0'] - 1

# Convert years to integer
us_full_data['year_0'] = us_full_data['year_0'].astype(int)
us_full_data['relative_year'] = us_full_data['relative_year'].astype(int)
us_full_data['year_minus_1'] = us_full_data['year_minus_1'].astype(int)
# Print the data to verify the steps
print("Data after identifying Year 0, relative year, and Year -1:\n", us_full_data.head(32))
print()

# Extract BVE for the year before Year 0 (relative_year = -1) for deflation
bve_deflation = us_full_data[us_full_data['relative_year'] == -1][['isin', 'bve']].rename(columns={'bve': 'bve_deflation'})
print(bve_deflation)
# Merge the bve_deflation values back to the filtered data
filtered_data = filtered_data.merge(bve_deflation, on='isin', how='left')
print("Filtered data with bve_deflation:\n",filtered_data) # new column on bve_deflation
print()

# Calculate the BVE of the previous year for each year (for residual income calculation)
us_full_data['bve_prev'] = us_full_data.groupby('isin')['bve'].shift(1)
# Merge bve_prev back to filtered_data
filtered_data = filtered_data.merge(us_full_data[['isin', 'year_', 'bve_prev']], on=['isin', 'year_'], how='left')
print("Filtered data with bve_prev:\n",filtered_data) # new column on bve_prev
print()

# Function to calculate non-deflated residual income
def calculate_residual_income(row):
    return row['ninc'] - (cost_of_equity * row['bve_prev'])
# Apply the function to calculate non-deflated residual income for each row
filtered_data['residual_income'] = filtered_data.apply(calculate_residual_income, axis=1) 
# Display the 'residual_income' values
print("Residual income values:\n", filtered_data) # new column on residual_income
print()

# Function to deflate residual income
def deflate_residual_income(row):
    if pd.notna(row['bve_deflation']) and row['bve_deflation'] != 0:
        return row['residual_income'] / row['bve_deflation']
    else:
        return np.nan
# Apply the function to deflate residual income for each row
filtered_data['deflated_residual_income'] = filtered_data.apply(deflate_residual_income, axis=1)
print("Deflated residual income values:\n", filtered_data) # new column on deflated_residual_income
print()


'''
Step 7
'''
# Output the replicated table

# Group by P/B group and relative year, then calculate the median deflated residual income for each group and year
median_residual_income = filtered_data.groupby(['p/b_group', 'relative_year'], observed=True)['deflated_residual_income'].median().unstack()

# Formatting the results (decimal places)
median_residual_income = median_residual_income.apply(lambda col: col.map(lambda x: f"{x:.3f}" if pd.notna(x) else "NaN"))
median_pb_values = median_pb_values.apply(lambda x: f"{x:.2f}")

# Add the median P/B values column to the output table
median_residual_income.insert(0, 'P/B', median_pb_values)

# Print the median residual income table
print("Median Residual Income by P/B Group and Relative Year:\n", median_residual_income)
print()

# Save the results to an Excel file 
median_residual_income.to_excel('output/median_residual_income.xlsx')


'''
Step 8
'''
#  Modification: exclude negative and very high P/B values

# Filter out extreme P/B values that are negative and higher than 7
filtered_year_0_data = year_0_data[(year_0_data['p/b'] > 0) & (year_0_data['p/b'] <= 7)]
print("Filtered Year 0 data after excluding negative and very high P/B values:\n", filtered_year_0_data)
print()

# Recalculate the P/B groups based on the filtered data
filtered_year_0_data = filtered_year_0_data.sort_values('p/b', ascending=False).reset_index(drop=True)
filtered_year_0_data['p/b_group'] = pd.qcut(filtered_year_0_data.index, num_groups, labels=range(1, num_groups + 1))
print("Filtered Year 0 data updated with P/B groups:\n",filtered_year_0_data)
print()


# Merge the P/B groups back to the filtered data for Year 0
filtered_data = filtered_data.drop(columns=['p/b_group'])
filtered_data = filtered_data.merge(filtered_year_0_data[['isin', 'p/b_group']], on='isin', how='left')
filtered_data['p/b_group'] = filtered_data.groupby('isin')['p/b_group'].ffill()

# Calculate median P/B values again
median_pb_values = filtered_year_0_data.groupby('p/b_group', observed=True)['p/b'].median()

# Group by P/B group and relative year, then calculate the median deflated residual income for each group and year
median_residual_income_filtered = filtered_data.groupby(['p/b_group', 'relative_year'], observed=True)['deflated_residual_income'].median().unstack()

# Formatting the results (decimal places)
median_residual_income_filtered = median_residual_income_filtered.apply(lambda col: col.map(lambda x: f"{x:.3f}" if pd.notna(x) else "NaN"))
median_pb_values = median_pb_values.apply(lambda x: f"{x:.2f}")

# Add the median P/B values column to the output table
median_residual_income_filtered.insert(0, 'P/B', median_pb_values)

# Print the median residual income table
print("Median Residual Income by P/B Group and Relative Year:\n", median_residual_income_filtered)

# Save the results to an Excel file
median_residual_income_filtered.to_excel('output/median_residual_income_filtered.xlsx')