#!/bin/bash

# Assign arguments to variables
num_of_runs=$1

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <num_of_runs>"
    exit 1
fi

parent_dir=TCP_fg_BBR_bg_CUBIC
queue_size_mb=("0.5" "1" "1.5" "2" "2.5" "3" "3.5" "4" "4.5" "5" "5.5" "6" "7" "7.5" "8.5" "10" "11" "12.5" "15" "17.5" "20" "50")
queue_size_bytes=("524288" "1048576" "1572864" "2097152" "2621440" "3145728" "3670016" "4194304" "4718592" "5242880" "5767168" "6291456" "7340032" "7864320" "8912896" "10485760" "11534336" "13107200" "15728640" "18350080" "20971520" "52428800")

mkdir $parent_dir
echo "Create directory: /users/prajneet/$dir"

echo "Switching CCA to BBR on 192.168.X.11 machines"
sudo sysctl -w net.ipv4.tcp_congestion_control=bbr
ssh prajneet@192.168.254.11 "sudo sysctl -w net.ipv4.tcp_congestion_control=bbr"

echo "Starting the servers on both the machines"
ssh prajneet@192.168.254.11 "pkill iperf3"
ssh prajneet@192.168.254.31 "pkill iperf3"
ssh prajneet@192.168.254.11 "iperf-reliable/src/iperf3 -s -F /dev/null -d -r 2>&1 &" 2>&1 &
ssh prajneet@192.168.254.31 "iperf-reliable_bg/src/iperf3 -s -F /dev/null -d -r 2>&1 &" 2>&1 &
sleep 5

for i in "${!queue_size_bytes[@]}"
do
	dir="$parent_dir/${queue_size_mb[i]}MB_queue"
	mkdir $dir
	echo "changing queue size to ${queue_size_mb[i]} MB"
	source /proj/FEC-HTTP/nenv/bin/activate
	python3 /proj/FEC-HTTP/long-quic/long-look-quic/test_src/dumbbell_traffic_shaping.py 1000 20 0 "${queue_size_bytes[i]}"
	deactivate
	sleep 10
	for((i = 1; i <=num_of_runs; i++))
	do
		echo "Starting iteration $i of $num_of_runs..."


		# Use iperf-reliable to transfer file
		echo "Starting file transfer to $receiver_IP_address using iperf-reliable"
		ssh prajneet@192.168.253.31 "iperf-reliable_bg/src/iperf3 -t 600 -c 192.168.254.31 -F /dev/random 2>&1 &" 2>&1 & 
		iperf-reliable/src/iperf3 -t 600 -c 192.168.254.11 -F /dev/random 

		# Check if the file transfer was successful
		if [ $? -eq 0 ]; then
			echo "File transfer completed successfully (Iteration $i)."
		else
			echo "File transfer failed (Iteration $i). Aborting script."
			exit 1
		fi
	
		sleep 10

		mv "/users/prajneet/iperf_reliable_results/get_results_fg.json" "$dir/get_results_"$i"_fg.json"
		mv "/users/prajneet/iperf_reliable_results/send_results_fg.json" "$dir/send_results_"$i"_fg.json"
		mv "/users/prajneet/iperf_reliable_results/get_results_bg.json" "$dir/send_results_"$i"_bg.json"
		mv "/users/prajneet/iperf_reliable_results/send_results_bg.json" "$dir/get_results_"$i"_bg.json"

		echo "Iteration $i of $num_of_runs completed successfully."

	done

done
ssh prajneet@192.168.254.11 "pkill iperf3"
ssh prajneet@192.168.254.31 "pkill iperf3"

echo "Switching CCA back to CUBIC on 192.168.X.11 machines"
ssh prajneet@192.168.254.11 "sudo sysctl -w net.ipv4.tcp_congestion_control=cubic"
sudo sysctl -w net.ipv4.tcp_congestion_control=cubic
