#!/bin/sh
#
# This script:
#   creates directory /opt/pivotal/gemfire
#   copies file gemfire_validation_doc.md to directory /opt/pivotal/gemfire/
#   creates the motd

set -e

echo "### Starting script $0 .........."

INSTALL_DIR="/opt/pivotal/gemfire"
[[ ! -d ${INSTALL_DIR} ]] && { mkdir -p $INSTALL_DIR; chown gfadmin:gfadmin ${INSTALL_DIR}; }

mv /home/gfadmin/gemfire-azure/gemfire_validation_doc.md /opt/pivotal/gemfire/gemfire_validation_doc.md

gemfire_version=$(ls  -r /usr/local/ | grep pivotal-gemfire)

cat << _EOF > $INSTALL_DIR/motd
*********************************************************************************
Welcome to your Pivotal Gemfire in-memory Data Grid on Azure!
*********************************************************************************
Gemfire Version:  $gemfire_version

Display DNS names and IP addresses 
   - From the Linux command prompt:  cat /etc/hosts

Run some validation steps to get started
   - The document "gemfire_validation_doc.md" can be used to validate Gemfire as 
     well as provide an introduction to some of the GemFire cli (gfsh) commands. 
     Run the following to Read the validation doc:    
       cat /opt/pivotal/gemfire/gemfire_validation_doc.md | more

Connect to Gemfire cli
   - As user gfadmin, from the Linux command prompt:  gfsh

Connect to Gemfire Pulse
     http://[server0_ip_or_dns_name]:17070/pulse
     User ID and PWD: admin/admin

Gemfire Documentation
   - Getting Started with Gemfire: http://gemfire.docs.pivotal.io/gemfire/getting_started/book_intro.html
   - Gemfire Documentation: http://gemfire.docs.pivotal.io/gemfire/about_gemfire.html
   - Gemfire Pulse Overview: http://gemfire.docs.pivotal.io/geode/tools_modules/pulse/pulse-overview.html

Learn more about Gemfire
   - Gemfire 30 second review: https://www.youtube.com/watch?v=AEpILFGX8y0
   - Introduction to Gemfire Product Features: https://www.youtube.com/watch?v=q52QlWkdFgE
*********************************************************************************
_EOF

cmd="mv $INSTALL_DIR/motd /etc/motd"
echo $cmd
eval $cmd

echo "### Leaving script $0 .........."
