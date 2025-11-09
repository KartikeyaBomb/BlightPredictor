import matplotlib.pyplot as plt
import csv
from datetime import datetime
from collections import defaultdict
import os

# Directory containing neighborhood CSV files
hoods_dir = 'hoods'

# Neighborhood files
neighborhood_files = {
    'Parkway Village': 'Parkway_Village.csv',
    'Orange Mound': 'Orange_Mound.csv',
    'Frayser': 'Frayser.csv',
    'Egypt': 'Egypt.csv'
}

# Store incidents by month for each neighborhood
neighborhood_monthly_data = {}

print("=" * 80)
print("READING NEIGHBORHOOD DATA (JAN 2021 - DEC 2022)")
print("=" * 80)

# Read each neighborhood's CSV file
for neighborhood, filename in neighborhood_files.items():
    filepath = os.path.join(hoods_dir, filename)
    
    monthly_counts = defaultdict(int)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            
            for row in reader:
                # Extract year and month from reported_date
                date = datetime.strptime(row['reported_date'], '%Y-%m-%d')
                
                # Only include data from Jan 2021 to Dec 2022
                if datetime(2021, 1, 1) <= date <= datetime(2022, 12, 31):
                    year_month = date.strftime('%Y-%m')  # Format: "2021-01"
                    monthly_counts[year_month] += 1
        
        neighborhood_monthly_data[neighborhood] = monthly_counts
        total = sum(monthly_counts.values())
        print(f"✓ Loaded {neighborhood}: {total} incidents (Jan 2020 - Dec 2022)")
        
    except FileNotFoundError:
        print(f"✗ File not found: {filepath}")

# Generate all months from Jan 2021 to Dec 2022
all_months = []
current_date = datetime(2021, 1, 1)
end_date = datetime(2022, 12, 31)

while current_date <= end_date:
    all_months.append(current_date.strftime('%Y-%m'))
    # Move to next month
    if current_date.month == 12:
        current_date = datetime(current_date.year + 1, 1, 1)
    else:
        current_date = datetime(current_date.year, current_date.month + 1, 1)

print("\n" + "=" * 80)
print("CREATING MONTHLY PLOT")
print("=" * 80)

# Create the plot
plt.figure(figsize=(16, 8))

# Plot each neighborhood
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
for idx, (neighborhood, monthly_counts) in enumerate(neighborhood_monthly_data.items()):
    # Get counts for all months (0 if no incidents)
    counts = [monthly_counts.get(month, 0) for month in all_months]
    
    plt.plot(range(len(all_months)), counts, marker='o', linewidth=2, markersize=6, 
             label=neighborhood, color=colors[idx], alpha=0.8)

# Format x-axis labels to show every 3 months
tick_positions = range(0, len(all_months), 3)
tick_labels = [all_months[i] for i in tick_positions]

plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Number of Incidents', fontsize=12, fontweight='bold')
plt.title('Service Request Incidents by Month (Jan 2021 - Dec 2022) - Memphis Neighborhoods', 
          fontsize=14, fontweight='bold')
plt.legend(loc='best', fontsize=10)
plt.grid(True, alpha=0.3)
plt.xticks(tick_positions, tick_labels, rotation=45, ha='right')
plt.tight_layout()

# Save the plot
output_file = 'incidents_by_month_2021_2022.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ Plot saved as: {output_file}")

# Show the plot
plt.show()

# Print summary statistics
print("\n" + "=" * 80)
print("SUMMARY STATISTICS (JAN 2021 - DEC 2022)")
print("=" * 80)

for neighborhood, monthly_counts in neighborhood_monthly_data.items():
    total = sum(monthly_counts.values())
    if total > 0:
        avg_per_month = total / 24  # 24 months
        print(f"\n{neighborhood}:")
        print(f"  Total incidents: {total}")
        print(f"  Average per month: {avg_per_month:.1f}")
        
        # Find peak month
        peak_month = max(monthly_counts, key=monthly_counts.get)
        peak_count = monthly_counts[peak_month]
        print(f"  Peak month: {peak_month} ({peak_count} incidents)")

print("\nPlot created successfully!")