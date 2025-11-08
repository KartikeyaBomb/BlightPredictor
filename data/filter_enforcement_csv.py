#!/usr/bin/env python3
"""
Filter historical-code-enforcement-requests.csv to only include specific categories.
"""

import pandas as pd

# Read the CSV
input_file = 'data/historical-code-enforcement-requests.csv'
output_file = 'data/historical-code-enforcement-requests-filtered.csv'

print(f"Reading {input_file}...")
df = pd.read_csv(input_file, delimiter=';')

print(f"Total rows: {len(df)}")

# Define the categories to filter
categories_to_keep = [
    'Cleanup',
    'Inspection-Junky Yard',
    'Inspection-Vacant Violation',
    'Weeds'
]

# Filter the dataframe
filtered_df = df[df['category'].isin(categories_to_keep)]

print(f"\nFiltered rows: {len(filtered_df)}")
print(f"Removed rows: {len(df) - len(filtered_df)}")

# Show category breakdown
print("\nCategory breakdown:")
print(filtered_df['category'].value_counts())

# Save the filtered CSV
print(f"\nWriting to {output_file}...")
filtered_df.to_csv(output_file, index=False, sep=';')

print(f"Done! Created {output_file}")
