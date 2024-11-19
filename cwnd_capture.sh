#!/bin/bash

# Define the IP of the target connection
TARGET_IP=$1

# Output file to save cwnd sizes
OUTPUT_FILE=$2

# Clear the log file at the beginning
echo "Timestamp,cwnd,ssthresh" > "$OUTPUT_FILE"

# Loop to capture the cwnd size every second
while true; do
	timestamp=$(date +%s.%N | awk '{printf "%.6f", $1}')
    # Get all connections to the specified target IP with their cwnd and ssthresh values
    ss -i dst $TARGET_IP | awk -v timestamp="$timestamp" '
    /cwnd/ {
        match($0, /cwnd:[0-9]+/, cwnd) # Match cwnd value
		match($0, /ssthresh:([0-9]+)/, ssthresh) # Capture ssthresh value

        # Print in structured format only if both cwnd and ssthresh are found
        if (cwnd[0]) {
            print timestamp "," substr(cwnd[0],6) "," substr(ssthresh[0],10)
        }
    }' >> "$OUTPUT_FILE"

    # Wait for 1 second before the next capture
    #sleep 1
done

