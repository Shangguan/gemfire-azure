from __future__ import print_function
import subprocess


if __name__ == '__main__':
    """
    This script creates a file system on /dev/sdc, mounts it and
    creates an fstab entry.

    !! It currently handles only one data disk. !!

    !! It does not check for the presence of data before formatting !!

    It must be run as root.

    This script requires no environment variables
    """
    device = '/dev/sdc'
    mount_point = '/datadisks/disk1'
    fstype = 'ext4'

    # they seem to start off mounted so unmount first
    subprocess.call(['umount', device + '1'])

    subprocess.check_output(['parted', '-s', device, 'mklabel', 'gpt', 'mkpart', 'primary', 'ext2', '0%', '100%'])
    print('partitioned {0}'.format(device))

    # wait for /dev/sdc1 to be created
    subprocess.call(['sleep','5'])

    subprocess.check_call(['mkfs','-t',fstype, device + '1'])
    print('formatted {0}'.format(device))

    subprocess.check_call(['mkdir','-p',mount_point])
    subprocess.check_call(['mount','-t',fstype,device + '1',mount_point])
    print('mounted {0} on {1}'.format(device,mount_point))

    fstab_entry = '{0}  {1} {2} defaults 0 0'.format(device + '1',mount_point,fstype)
    with open('/etc/fstab','a') as fstab_file:
        fstab_file.write('\n' + fstab_entry)

    print('updated fstab for {0}'.format(device + '1'))
