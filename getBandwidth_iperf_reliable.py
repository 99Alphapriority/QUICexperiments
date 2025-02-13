import sys
import scipy.stats as stats
import numpy as np
import pandas as pd
import json
from pprint import pprint

cca = ['CUBIC', 'BBR']

mainDir = sys.argv[1]
total_runs = int(sys.argv[2])

# Create an excel file
excel_file = mainDir + "bandwidth.xlsx"

# Use a single ExcelWriter object to write all sheets to the same file
with pd.ExcelWriter(excel_file) as writer:
    for cca_bg in cca:
        for cca_fg in cca:
            bandwidth = []
            for expNo in range(1, total_runs + 1):
                file_name = mainDir + "TCP_fg_" + cca_fg + "_bg_" + cca_bg + "/get_results_" + str(expNo) + ".json"
                try:
                    with open(file_name, 'r') as f:
                        j = json.load(f)
                        bytes_transfered = j['streams'][0]['bytes']
                        end_time = j['streams'][0]['end_time']
                        affective_bandwidth = (((bytes_transfered) * 8 ) / (1000 * 1000)) / end_time #convert the bandwidth to Mbps
                        bandwidth.append(affective_bandwidth)
                except Exception as e:
                    print("Failed ", e)
                print(file_name)

            # Print the bandwidth for debugging
            for i in range(0, total_runs):
                print(bandwidth[i])

            print("\n")

            # Insert data into the DataFrame
            bandwidth_df = pd.DataFrame(bandwidth, columns=['bandwidth'])  # Reset DataFrame per combination

            # Define sheet name based on congestion control algorithms
            sheet_name = "TCP_fg_" + cca_fg + "_bg_" + cca_bg

            # Write the DataFrame to the specified sheet
            bandwidth_df.to_excel(writer, sheet_name=sheet_name, index=False)

