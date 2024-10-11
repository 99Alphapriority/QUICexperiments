sudo mkdir /mnt/send_file
sudo mount -t tmpfs -o size="$1G" tmpfs /mnt/send_file
let file_size=$1*1024
dd if=/dev/zero of="/mnt/send_file/$1GBfile" bs=1M count=$file_size
