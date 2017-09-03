#!/bin/sh
drives=($(ls -1 /dev/sd*|grep -E -v "[0-9]$"| grep -E -v "sda" | grep -E -v "sdb"))
count=1
fs_type=83
for targetdisk in "${drives[@]}";
do
        echo "Start processing the disk $targetdisk ..................."
        sudo su -c "echo 'n
p
1


t
${fs_type}
w'| fdisk '${targetdisk}' "
        echo "disk partitioning is finished for $targetdisk"
        partition=`sudo su -c "fdisk -l $targetdisk|grep -A 1 Device|tail -n 1"`
        echo "partition -> $partition"
        partition_id=`echo $partition | awk '{print $1}'`
        echo "making ext4 fs on partition -> $partition_id"
        sudo su -c "mkfs.ext3 ${partition_id} -O sparse_super,large_file -m 0 -T largefile4"
        mount_point="/datadisks/disk$count"
        echo "creating mount folder $mount_point ..............."
        sudo su -c "mkdir -p $mount_point"
        ((count = count + 1))
        uuid=`sudo su -c "blkid -u filesystem ${partition_id}|awk -F \"[= ]\" '{print $3}' | sed 's/\"//g'"`
        fstab_entry="UUID=${uuid}\t${mount_point}\text4\tdefaults\t0 0"
        echo "adding $fstab_entry to /etc/fstab ........."
        sudo su -c "echo -e '$fstab_entry' >> /etc/fstab"
        echo "mounting the paths ......"
        sudo su -c "mount $partition_id $mount_point"
        echo "Finished processing the disk $targetdisk ..................."
done