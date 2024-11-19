import sys
import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the Excel file
file_path = sys.argv[1]  # Replace with the path to your Excel file
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Assuming each row represents a time interval
time = range(len(data))  # Generate a time series based on the number of rows

df_sampled = data.iloc[::100, :]  # Keep every 500th data point
time_sampled = range(len(df_sampled))

# Plotting the congestion windows for foreground (cwnd_fg) and background (cwnd_bg)
plt.figure(figsize=(12, 6), dpi=120)
plt.plot(time_sampled, df_sampled['cwnd_fg'], label='Foreground (BBR)', color='red')
plt.plot(time_sampled, df_sampled['cwnd_bg'], label='Background (BBR)', color='blue')

# Labels, title, and legend
plt.xlabel('Time (s)')
plt.ylabel('Congestion Window (KB)')
plt.title('Congestion Window vs. Time')
plt.legend(loc='upper right')
plt.grid(True)

# Display the plot
plt.show()

