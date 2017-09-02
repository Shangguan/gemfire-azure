The scripts in this directory are used to initialize the vms after they
have been provisioned.  The initialization process is controlled by
_bootstrap.py_ which does the following.

* installs git if it is not present
* git clones this repository onto the a specified user's home
directory (this user must exist) and changes the owner to the that user.
* checks out a specified branch or tag (default is just master)
* uses input parameters to initialize a set of environment variables which
will be passed to each script
* runs all scripts in the _init\_scripts_ directory in sorted order
sending the output to /var/log/cloud-init.log
* each script will be provided with the environment variables and the
return code will be checked.  A non-zero return code will cause the process
to fail.

Both python and shell scripts are supported. Scripts must take all input in the
form of environment variables. Scripts should document the environment variables
they use.
