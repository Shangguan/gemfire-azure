#!/bin/sh
#
# This script expects the following environment variables
#
# GEMFIRE_USER  the user that will run the GemFire processes
# REGION_NAME   the azure region where this cluster is running (becomes part of the host name)
# GEMFIRE_VERSION either 8 or 9

# echo "applying sudo rules........"
# sed -i 's/Defaults\s\{1,\}requiretty/Defaults \!requiretty/g' /etc/sudoers
# echo "$GEMFIRE_USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

echo "disabling selinux ......"
setenforce 0
sed -i -e 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

echo "stopping iptables....."
systemctl stop firewall
sudo systemctl disable firewalld

echo "Installing wget ...."
yum install -y wget

echo "Installing ntp ....."
yum install -y ntp
systemctl start ntpd
systemctl enable ntpd

echo 'umask 0022' >> /etc/profile

echo "setting nohost check for ssh ..."

echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config
echo "UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config
systemctl restart sshd

echo "enabling epel repo....."
yum install -y epel-release
echo "install python-pip ......"
yum -y install python-pip
echo "install python jinja2 ..."
pip install jinja2

echo "installing jdk....."
wget https://gemfirestgacct01.blob.core.windows.net/binaries/jdk-8u144-linux-x64.rpm
yum localinstall -y jdk-8u144-linux-x64.rpm
rm -f jdk-8u102-linux-x64.rpm

echo "installing Gemfire software ........"
wget https://gemfirestgacct01.blob.core.windows.net/binaries/pivotal-gemfire-9.1.1.tar.gz
tar -xvf pivotal-gemfire-9.1.1.tar.gz
mv pivotal-gemfire-9.1.1 /usr/local/
ln -s /usr/local/pivotal-gemfire-9.1.1/ /usr/local/gemfire
chown -R $GEMFIRE_USER:$GEMFIRE_USER /usr/local/gemfire

echo export JAVA_HOME=/usr/java/jdk1.8.0_144 >> /home/$GEMFIRE_USER/.bashrc
echo export GEMFIRE=/usr/local/gemfire >> /home/$GEMFIRE_USER/.bashrc
echo export PATH='$JAVA_HOME/bin:$GEMFIRE/bin:$PATH' >> /home/$GEMFIRE_USER/.bashrc


echo "Finished executing 04_init_vms.sh"
