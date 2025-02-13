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
window_size_bg = 10000
window_size_fg = 10000
smaller_max = df_fg['Timestamp'].max()
tolerance = 0.01
df_bg_sampled = df_bg[df_bg['Timestamp'] <= (smaller_max + tolerance) ]

df_fg['Timestamp_s'] = pd.to_datetime(df_fg['Timestamp'], unit='s', errors='coerce')  # Convert seconds to datetime
df_bg_sampled['Timestamp_s'] = pd.to_datetime(df_bg_sampled['Timestamp'], unit='s', errors='coerce')  # Convert seconds to datetime

df_bg_sampled = df_bg_sampled.dropna(subset=['Timestamp_s']).sort_values('Timestamp_s').reset_index(drop=True)
df_fg = df_fg.dropna(subset=['Timestamp_s']).sort_values('Timestamp_s').reset_index(drop=True)

df_fg.set_index('Timestamp_s', inplace=True)
df_bg_sampled.set_index('Timestamp_s', inplace=True)

df_bg_sampled['Moving_avg'] = df_bg_sampled['cwnd'].rolling('10s').mean()
df_fg['Moving_avg'] = df_fg['cwnd'].rolling('10s').mean()
#df_fg_sampled = df_fg.iloc[::2000, :]  # Keep every 500th data point
#df_bg_sampled = df_bg.iloc[::2000, :]
print(len(df_fg))
print(len(df_bg))

plt.plot(df_fg['Timestamp'], df_fg['cwnd'], label='Foreground (CUBIC)', alpha=0.7, color='blue', linestyle='-')
plt.plot(df_fg['Timestamp'], df_fg['Moving_avg'], label='Foreground Moving Average (10s) (CUBIC)', alpha=0.7, color='red', linestyle='-')
#plt.plot(df_fg_sampled['Timestamp'], df_fg_sampled['cwnd'], label='Foreground (CUBIC)', color='red', linestyle='-')
plt.plot(df_bg_sampled['Timestamp'], df_bg_sampled['cwnd'], label='Background (BBR)', alpha=0.7, color='orange', linestyle='-')
plt.plot(df_bg_sampled['Timestamp'], df_bg_sampled['Moving_avg'], label='Background Moving Average (10s) (BBR)', alpha=0.7, color='green', linestyle='-')
#plt.plot(df_bg_sampled['Timestamp'], df_bg_sampled['cwnd'], label='Background (BBR)', color='blue', linestyle='-')

# Plot the 'cwnd' (converted to Mbits) vs. 'time'
'''
plt.plot(df_fg['Timestamp'], df_fg['cwnd'], label='Foreground (BBR)', color='blue', linestyle='-')
plt.plot(df_bg['Timestamp'], df_bg['cwnd'], label='Background (CUBIC)', color='red', linestyle='-')
'''
#plt.axhline(y=5, color='black', linestyle='--', linewidth=1, label="5 Mbps Threshold")
#plt.axhline(y=2.5, color='black', linestyle='--', linewidth=1, label="2.5 Mbps Threshold")
# Adding labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('cwnd (Mbits)')
plt.title('cwnd vs Time with contention and TCP delayed ACK disabled (20*BDP (50MB) queue size)')
plt.grid(True)
#plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)
plt.tight_layout()
# Show the plot
plt.show()
