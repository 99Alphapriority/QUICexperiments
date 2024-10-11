sudo mkdir /mnt/recv_file
sudo mount -t tmpfs -o size="$1G" tmpfs /mnt/recv_file
