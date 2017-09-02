from __future__ import print_function
import os
import pwd

if __name__ == "__main__":
    cwd = os.getcwd()
    uname = pwd.getpwuid(os.getuid())[0]
    with open('/var/log/cloud-init.log','w') as log:
        log.write('I am the bootstrap running in {0} as {1}. Peace out.\n'.format(cwd, uname))
