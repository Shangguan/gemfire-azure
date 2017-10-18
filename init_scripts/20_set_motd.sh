#!/bin/sh
#
# This script creates the motd

set -e

echo "### Starting script $0 .........."

INSTALL_DIR="/opt/pivotal/gemfire"
[[ ! -d ${INSTALL_DIR} ]] && { mkdir -p $INSTALL_DIR; chown gfadmin:gfadmin ${INSTALL_DIR}; }

gemfire_version=$(ls  -r /usr/local/ | grep pivotal-gemfire)

cat << _EOF > $INSTALL_DIR/motd
*********************************************************************************
Welcome to your Pivotal Gemfire in-memory Data Grid on Azure!
*********************************************************************************
Gemfire Version:  $gemfire_version

Display Gemfire Host names and IP addresses 
   - From the Linux command prompt:  cat /etc/hosts

Connect to Gemfire cli
   - As user gfadmin, from the Linux command prompt:  gfsh

Connect to Gemfire Pulse
     http://[server0_ip_or_dns_name]:17070/pulse
     User ID and PWD: admin/admin

Gemfire Documentation
   - Pivotal Home: https://pivotal.io
   - Gemfire Pulse Overview: http://gemfire.docs.pivotal.io/geode/tools_modules/pulse/pulse-overview.html
   - Gemfire Documentation: http://gemfire.docs.pivotal.io/gemfire/about_gemfire.html
   - Gemfire Documentation pdf version: http://gemfire.docs.pivotal.io/pdf/pivotal-gemfire-91.pdf

Learn more about Gemfire
   - Gemfire 30 second review: https://www.youtube.com/watch?v=AEpILFGX8y0
   - Introduction to Gemfire Product Features: https://www.youtube.com/watch?v=q52QlWkdFgE

Validation steps
   - See file: gemfire_validation.txt located: /opt/pivotal/gemfire
*********************************************************************************
_EOF

cmd="mv $INSTALL_DIR/motd /etc/motd"
echo $cmd
eval $cmd

echo "### Leaving script $0 .........."



