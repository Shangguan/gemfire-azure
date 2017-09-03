#!/bin/sh
ADMINUSER=$1
REGION_NAME=$2
GEMFIRE_VERSION=$3

echo "applying sudo rules........"
sed -i 's/Defaults\s\{1,\}requiretty/Defaults \!requiretty/g' /etc/sudoers
echo "$ADMINUSER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

echo "disabling selinux ......"
setenforce 0
sed -i -e 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

echo "stopping iptables....."
systemctl stop firewall
sudo systemctl disable firewalld

echo "Installing wget ...."
yum insall -y wget

echo "Installing ntp ....."
yum install -y ntp
systemctl start ntpd
systemctl enable ntpd


echo "setting private ip and public host name mappings ......"
host=$(hostname)
ipaddr=$(hostname -I)
echo "$ipaddr $host.$REGION_NAME.cloudapps.azure.com $host" >> /etc/hosts


echo 'umask 0022' >> /etc/profile

echo "setting nohost check for ssh ..."

echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config
echo "UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config
systemctl restart sshd

echo "Peparing Disks.... "
chmod ugo+rx prepare_data_disks.sh
sh prepare_data_disks.sh

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

if [ "$GEMFIRE_VERSION" == 8 ]
then
        wget https://gemfirestgacct01.blob.core.windows.net/binaries/Pivotal_GemFire_826_b41_Linux.tar.gz
        tar -xvf Pivotal_GemFire_826_b41_Linux.tar.gz
		mv Pivotal_GemFire_826_b41_Linux /usr/local/
		ln -s /usr/local/Pivotal_GemFire_826_b41_Linux/ /usr/local/gemfire
		chown -R $ADMINUSER:$ADMINUSER /usr/local/gemfire
elif [ "$GEMFIRE_VERSION" == 9 ]
then
        wget https://gemfirestgacct01.blob.core.windows.net/binaries/pivotal-gemfire-9.1.0.tar.gz
        tar -xvf pivotal-gemfire-9.1.0.tar.gz
		mv pivotal-gemfire-9.1.0 /usr/local/
		ln -s /usr/local/pivotal-gemfire-9.1.0/ /usr/local/gemfire
		chown -R $ADMINUSER:$ADMINUSER /usr/local/gemfire
else
        echo "Did not understood the version, not installing Gemfire ....."
fi
		
echo "export JAVA_HOME=/usr/java/jdk1.8.0_144" >> /home/$ADMINUSER/.bashrc
echo "export GEMFIRE_HOME=/usr/local/gemfire" >> /home/$ADMINUSER/.bashrc
echo "export PATH=$JAVA_HOME/bin:$GEMFIRE_HOME/bin:$PATH" >> /home/$ADMINUSER/.bashrc

		
echo "Finished executing the Init_HdpVM."