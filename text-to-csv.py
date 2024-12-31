import pandas as pd

# Define input and output file paths
input_file = "data/raw/MachineLearningRating_v3.txt"  
output_file = "data/raw/MachineLearningRating_v3.csv"  

# Read the text file with '|' delimiter
data = pd.read_csv(input_file, delimiter='|')  # Assuming '|' is the delimiter

# Save the data to a CSV file
data.to_csv(output_file, index=False)

print(f"File successfully converted and saved as {output_file}")