import pandas as pd

# Load CSV
try:
    df = pd.read_csv('Stacked_Filtered_Modes_Pitch_Classes_Chart.csv')
except FileNotFoundError:
    print("Error: CSV file not found. Ensure 'Stacked_Filtered_Modes_Pitch_Classes_Chart.csv' exists.")
    exit(1)

# Calculate start_column from Weighting Function, with error handling
def get_start_column(weight):
    try:
        return 12 - len(str(weight).lstrip('9'))
    except (TypeError, ValueError):
        return -1  # Flag invalid entries

df['start_column'] = df['Weighting Function'].apply(get_start_column)

# Filter out invalid start_column values
df = df[df['start_column'].between(0, 12)]

# Count non-empty PCs in [start_column, 12] for each row
def count_pcs(row):
    start = row['start_column']
    pc_columns = [f'PC{i}' for i in range(int(start), 13)]
    return sum(1 for col in pc_columns if pd.notna(row[col]) and row[col] and row[col] != 'xxx')

df['pc_count'] = df.apply(count_pcs, axis=1)

# Filter for exactly 3 PCs
exactly_3_pcs = df[df['pc_count'] == 3]

# Count rows and group by start_column
total_rows = len(exactly_3_pcs)
print(f"Total rows with exactly 3 PCs: {total_rows}")
if total_rows > 0:
    print("\nBy start_column:")
    print(exactly_3_pcs.groupby('start_column').size())
else:
    print("No rows with exactly 3 PCs found.")