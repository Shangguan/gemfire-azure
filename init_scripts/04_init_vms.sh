#!/bin/sh
#
# This script expects the following environment variables
#
# GEMFIRE_USER  the user that will run the GemFire processes
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
sudo yum install -y java-1.8.0-openjdk-devel

echo "installing Gemfire software ........"
wget http://download.pivotal.com.s3.amazonaws.com/gemfire/9.2.2/pivotal-gemfire-9.2.2.zip
unzip pivotal-gemfire-9.2.2.zip
mv pivotal-gemfire-9.2.2 /usr/local/
ln -s /usr/local/pivotal-gemfire-9.2.2/ /usr/local/gemfire
chown -R $GEMFIRE_USER:$GEMFIRE_USER /usr/local/gemfire

echo export JAVA_HOME=/etc/alternatives/java_sdk >> /home/$GEMFIRE_USER/.bashrc
echo export GEMFIRE=/usr/local/gemfire >> /home/$GEMFIRE_USER/.bashrc
echo export PATH='$JAVA_HOME/bin:$GEMFIRE/bin:/usr/local/maven/bin:$PATH' >> /home/$GEMFIRE_USER/.bashrc

source  /home/$GEMFIRE_USER/.bashrc


echo "Finished executing 04_init_vms.sh"
