#!/bin/bash

# Assign arguments to variables
src_file_path=$1
receiver_IP_address=$2
num_of_runs=$3
dest_file_path=$4
output_dir=$5

if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <src_file_path> <receiver_IP_address> <num_of_runs> <dest_file_path> <output_dir>"
    exit 1
fi

mkdir $output_dir

# Compute and store the MD5SUM of the file to send
src_file_md5=$(md5sum "$src_file_path" | awk '{ print $1 }')
echo "src file $src_file_path md5sum: $src_file_md5"

# Loop N times
for ((i=1; i<=num_of_runs; i++))
do
	echo "Starting iteration $i of $num_of_runs..."

	# Use iperf-reliable to transfer file
	echo "Starting file transfer to $receiver_IP_address using iperf-reliable"
	iperf-reliable/src/iperf3 -c "$receiver_IP_address" -F "$src_file_path"

	# Check if the file transfer was successful
	if [ $? -eq 0 ]; then
		echo "File transfer completed successfully (Iteration $i)."
	else
		echo "File transfer failed (Iteration $i). Aborting script."
	exit 1
	fi

	# SSH into the server and compute the MD5 checksum of the transferred file
	echo "Verifying MD5 checksum on remote server (Iteration $i)..."
	dest_file_md5=$(ssh prajneet@"$receiver_IP_address" "md5sum $dest_file_path | awk '{ print \$1 }'")
	
	#Compare the expected and received MD5SUM
	if [ "$dest_file_md5" != "$src_file_md5" ]; then
		echo "MD5 checksum on the remote server does not match (Iteration $i). Aborting script."
		exit 1
	else
		echo "MD5 checksum matches on the remote server (Iteration $i)!"
	fi

	# SSH into the server and delete the file after the checksum check
    	echo "Deleting the file on the remote server (Iteration $i)..."
    	ssh prajneet@"$receiver_IP_address" "rm -f $dest_file_path"
    
    	# Check if the deletion was successful
	if [ $? -eq 0 ]; then
		echo "File deleted successfully from remote server (Iteration $i)."
	else
		echo "Failed to delete file from remote server (Iteration $i)."
        exit 1
	fi

	mv "/users/prajneet/iperf_reliable_results/get_results.json" "$output_dir/get_results_$i.json"
	mv "/users/prajneet/iperf_reliable_results/send_results.json" "$output_dir/send_results_$i.json"

	echo "Iteration $i of $num_of_runs completed successfully."
done

echo "All $num_of_runs iterations completed successfully!"
