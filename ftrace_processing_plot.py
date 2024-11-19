import sys
import pandas as pd
import matplotlib.pyplot as plt

plt.clf()
plt.cla()
plt.close()

# Load the data from the Excel file
file_path_fg = sys.argv[1]
file_path_bg = sys.argv[2]

temp_fg = pd.read_csv(file_path_fg, header=None, names=['Timestamp', 'cwnd'] , nrows=2)
temp_bg = pd.read_csv(file_path_bg, header=None, names=['Timestamp', 'cwnd'] , nrows=2)
start_time_fg = float(temp_fg['Timestamp'].iloc[1])
start_time_bg = float(temp_bg['Timestamp'].iloc[1])

# Define the conversion factor to convert cwnd to Mbits
conversion_factor = (1448 * 8) / (1000 * 1000)  # Convert bytes to Mbits

# Create an empty list to collect the processed chunks
processed_chunks_fg = []
processed_chunks_bg = []

# Read the CSV file in chunks
chunk_size = 10000  # Adjust based on your memory size and dataset
for chunk_fg in pd.read_csv(file_path_fg, chunksize=chunk_size, header=None, names=['Timestamp', 'cwnd']):

	# Ensure the 'Timestamp' column is of float type (to prevent errors during subtraction)
    chunk_fg['Timestamp'] = pd.to_numeric(chunk_fg['Timestamp'], errors='coerce')

	# Ensure the 'cwnd' column is numeric (convert any invalid entries to NaN)
    chunk_fg['cwnd'] = pd.to_numeric(chunk_fg['cwnd'], errors='coerce')

    # Multiply 'cwnd' column by the conversion factor
    chunk_fg['cwnd'] = chunk_fg['cwnd'] * conversion_factor

	# Normalize the 'time' column by subtracting the first timestamp
    chunk_fg['Timestamp'] = chunk_fg['Timestamp'] - start_time_fg

    # Optionally, append the processed chunk to the list
    processed_chunks_fg.append(chunk_fg)

for chunk_bg in pd.read_csv(file_path_bg, chunksize=chunk_size, header=None, names=['Timestamp', 'cwnd']):

    # Ensure the 'Timestamp' column is of float type (to prevent errors during subtraction)
    chunk_bg['Timestamp'] = pd.to_numeric(chunk_bg['Timestamp'], errors='coerce')

    # Ensure the 'cwnd' column is numeric (convert any invalid entries to NaN)
    chunk_bg['cwnd'] = pd.to_numeric(chunk_bg['cwnd'], errors='coerce')

    # Multiply 'cwnd' column by the conversion factor
    chunk_bg['cwnd'] = chunk_bg['cwnd'] * conversion_factor

    # Normalize the 'time' column by subtracting the first timestamp
    chunk_bg['Timestamp'] = chunk_bg['Timestamp'] - start_time_bg

    # Optionally, append the processed chunk to the list
    processed_chunks_bg.append(chunk_bg)

# Combine all processed chunks into a single DataFrame
df_fg = pd.concat(processed_chunks_fg, ignore_index=True)
df_bg = pd.concat(processed_chunks_bg, ignore_index=True)

plt.figure(figsize=(12, 6), dpi=120)


df_fg_sampled = df_fg.iloc[::1000, :]  # Keep every 500th data point
df_bg_sampled = df_bg.iloc[::1000, :]
plt.plot(df_fg_sampled['Timestamp'], df_fg_sampled['cwnd'], label='Foreground (BBR)', color='red', linestyle='-')
plt.plot(df_bg_sampled['Timestamp'], df_bg_sampled['cwnd'], label='Background (BBR)', color='blue', linestyle='-')

# Plot the 'cwnd' (converted to Mbits) vs. 'time'
'''
plt.plot(df_fg['Timestamp'], df_fg['cwnd'], label='Foreground (BBR)', color='blue', linestyle='-')
plt.plot(df_bg['Timestamp'], df_bg['cwnd'], label='Background (CUBIC)', color='red', linestyle='-')
'''
# Adding labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('cwnd (Mbits)')
plt.title('cwnd vs Time')
plt.grid(True)
plt.legend()

# Show the plot
plt.show()
