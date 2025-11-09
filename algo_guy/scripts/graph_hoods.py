import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime
from collections import defaultdict

# Directories
evictions_dir = 'hoods_Evictions'
police_dir = 'hoods_Police'

# Neighborhoods
neighborhoods = ['Egypt', 'Frayser', 'Parkway_Village', 'Orange_Mound']

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

print("=" * 80)
print("READING EVICTION DATA")
print("=" * 80)

# Store eviction data by neighborhood and month
evictions_data = {neighborhood: defaultdict(int) for neighborhood in neighborhoods}

for neighborhood in neighborhoods:
    filename = f"{neighborhood}.csv"
    filepath = os.path.join(evictions_dir, filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            
            count = 0
            for row in reader:
                # Parse filing date
                filing_date = datetime.strptime(row['Filing Date'], '%Y-%m-%d')
                
                # Only include data from Jan 2021 to Dec 2022
                if datetime(2021, 1, 1) <= filing_date <= datetime(2022, 12, 31):
                    year_month = filing_date.strftime('%Y-%m')
                    evictions_data[neighborhood][year_month] += 1
                    count += 1
            
            print(f"✓ {neighborhood}: {count} evictions (Jan 2021 - Dec 2022)")
    
    except FileNotFoundError:
        print(f"✗ File not found: {filepath}")

print("\n" + "=" * 80)
print("READING POLICE DATA")
print("=" * 80)

# Store police data by neighborhood and month
police_data = {neighborhood: defaultdict(int) for neighborhood in neighborhoods}

for neighborhood in neighborhoods:
    filename = f"{neighborhood}.csv"
    filepath = os.path.join(police_dir, filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            count = 0
            for row in reader:
                # Parse offense date (format: 2021-02-19 02:00:00+00:00)
                offense_date = datetime.strptime(row['Offense Date'], '%Y-%m-%d %H:%M:%S%z')
                
                # Only include data from Jan 2021 to Dec 2022
                if datetime(2021, 1, 1) <= offense_date.replace(tzinfo=None) <= datetime(2022, 12, 31):
                    year_month = offense_date.strftime('%Y-%m')
                    police_data[neighborhood][year_month] += 1
                    count += 1
            
            print(f"✓ {neighborhood}: {count} incidents (Jan 2021 - Dec 2022)")
    
    except FileNotFoundError:
        print(f"✗ File not found: {filepath}")

print("\n" + "=" * 80)
print("CREATING PLOTS")
print("=" * 80)

# Colors for each neighborhood
colors = {
    'Egypt': '#1f77b4',
    'Frayser': '#ff7f0e',
    'Parkway_Village': '#2ca02c',
    'Orange_Mound': '#d62728'
}

# Plot 1: Evictions
fig1, ax1 = plt.subplots(figsize=(16, 8))

for neighborhood in neighborhoods:
    counts = [evictions_data[neighborhood].get(month, 0) for month in all_months]
    ax1.plot(range(len(all_months)), counts, marker='o', linewidth=2, markersize=6,
             label=neighborhood.replace('_', ' '), color=colors[neighborhood], alpha=0.8)

# Format x-axis labels to show every 3 months
tick_positions = range(0, len(all_months), 3)
tick_labels = [all_months[i] for i in tick_positions]

ax1.set_xlabel('Month', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Evictions', fontsize=12, fontweight='bold')
ax1.set_title('Eviction Filings by Month (Jan 2021 - Dec 2022) - Memphis Neighborhoods',
              fontsize=14, fontweight='bold')
ax1.legend(loc='best', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xticks(tick_positions)
ax1.set_xticklabels(tick_labels, rotation=45, ha='right')
plt.tight_layout()

# Save evictions plot
evictions_output = 'evictions_by_month_2021_2022.png'
plt.savefig(evictions_output, dpi=300, bbox_inches='tight')
print(f"✓ Evictions plot saved as: {evictions_output}")

# Plot 2: Police Incidents
fig2, ax2 = plt.subplots(figsize=(16, 8))

for neighborhood in neighborhoods:
    counts = [police_data[neighborhood].get(month, 0) for month in all_months]
    ax2.plot(range(len(all_months)), counts, marker='o', linewidth=2, markersize=6,
             label=neighborhood.replace('_', ' '), color=colors[neighborhood], alpha=0.8)

ax2.set_xlabel('Month', fontsize=12, fontweight='bold')
ax2.set_ylabel('Number of Incidents', fontsize=12, fontweight='bold')
ax2.set_title('Police Incidents by Month (Jan 2021 - Dec 2022) - Memphis Neighborhoods',
              fontsize=14, fontweight='bold')
ax2.legend(loc='best', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xticks(tick_positions)
ax2.set_xticklabels(tick_labels, rotation=45, ha='right')
plt.tight_layout()

# Save police plot
police_output = 'police_incidents_by_month_2021_2022.png'
plt.savefig(police_output, dpi=300, bbox_inches='tight')
print(f"✓ Police incidents plot saved as: {police_output}")

# Show both plots
plt.show()

print("\n" + "=" * 80)
print("SUMMARY STATISTICS (JAN 2021 - DEC 2022)")
print("=" * 80)

print("\nEVICTIONS:")
for neighborhood in neighborhoods:
    total = sum(evictions_data[neighborhood].values())
    if total > 0:
        avg = total / 24
        print(f"  {neighborhood.replace('_', ' ')}: {total} total (avg {avg:.1f}/month)")

print("\nPOLICE INCIDENTS:")
for neighborhood in neighborhoods:
    total = sum(police_data[neighborhood].values())
    if total > 0:
        avg = total / 24
        print(f"  {neighborhood.replace('_', ' ')}: {total} total (avg {avg:.1f}/month)")

print("\n✓ Plots created successfully!")