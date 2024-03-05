import matplotlib.pyplot as plt
import numpy as np

counts = [0] * 8
total_count = 0  # Initialize total count to calculate percentages

with open("/results/quantifyRepresentation/race.tsv", "r") as dataFile:
    for i, line in enumerate(dataFile):
        if i == 0:
            continue
        line = line.rstrip().split("\t")
        count = int(line[1])
        counts[int(line[0]) - 1] = count
        total_count += count  # Sum up the total count

# Convert counts to percentages
percentages = [(count / total_count) * 100 for count in counts]

# Data
categories = ["European", "African", "Hispanic/Latin American", "Asian", "Multiple Ancestry", "Greater Middle Eastern", "Native American", "Oceanian"]

# Combine categories and percentages, then sort
combined = list(zip(categories, percentages))
sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)  # Sort by percentage in descending order

# Unzip the sorted combined list back into sorted categories and percentages
sorted_categories, sorted_percentages = zip(*sorted_combined)

# Color-blind friendly color palette
colors = plt.cm.tab10(np.arange(len(categories))/len(categories))
print(colors[2])

# Set global font size for larger text
plt.rcParams.update({'font.size': 14})  # Adjust the size as needed

# Creating the bar plot
plt.figure(figsize=(10, 8))  # Adjust the figure size as needed
bars = plt.bar(sorted_categories, sorted_percentages, color=colors[0])

plt.xlabel('Ancestry Categories')  # Label for X-axis
plt.ylabel('Percent')  # Label for Y-axis
plt.title('Percent of Transcriptomic Samples by Ancestry Category')  # Title of the plot
plt.xticks(rotation=45, ha="right")  # Rotate category names for better readability

# Optional: Display the percentage values above each bar
for bar, percentage in zip(bars, sorted_percentages):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, "{:.1f}%".format(percentage), ha='center', va='bottom')

plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
plt.savefig("/results/quantifyRepresentation/race.jpg")
plt.show()
