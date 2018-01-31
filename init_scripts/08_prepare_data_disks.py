from __future__ import print_function
import subprocess


if __name__ == '__main__':
    """
    This script creates a file system on /dev/sdc, mounts it and
    creates an fstab entry.

    !! It currently handles on one data disk. !!

    It must be run as root.

    This script requires no environment variables
    """
    device = '/dev/sdc'
    mount_point = '/datadisks/disk1'
    fstype = 'ext4'

    subprocess.check_call(['mkfs','-t',fstype,device])
    print('formatted {0}'.format(device))

    subprocess.check_call(['mkdir','-p',mount_point])
    subprocess.check_call(['mount','-t',fstype,device,mount_point])

    fstab_entry = '{0}  {1} {2} default 0 0'.format(device,mount_point,fstype)
    with open('/etc/fstab','a') as fstab_file:
        fstab_file.write('\n' + fstab_entry)

    print('mounted {0} on {1}'.format(device,mount_point))
