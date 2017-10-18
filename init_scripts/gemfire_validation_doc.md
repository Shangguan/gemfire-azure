Gemfire on Azure 
Use the following steps to validate the functionality of Gemfire.  Performing these steps also provides an introduction to some of the gfsh cli commands.
The last section describes Pulse, including how to launch it and login.
Validate Gemfire on Azure 
Create a scratch working directory (for example, my_gemfire) and change to it. gfsh saves locator and server working directories and log files in this location.
mkdir my_gemfire
cd my_gemfire/

Now start gfsh at the command prompt

 gfsh
    _________________________     __
   / _____/ ______/ ______/ /____/ /
  / /  __/ /___  /_____  / _____  /
 / /__/ / ____/  _____/ / /    / /
/______/_/      /______/_/    /_/    9.1.1

Monitor and Manage Pivotal GemFire

Connect to a Gemfire locator
gfsh>connect --locator=rmpgf9-server0-data-platformengineering.eastus.cloudapp.azure.com[10000]

Connecting to Locator at [host=rmpgf9-server0-data-platformengineering.eastus.cloudapp.azure.com, port=10000] ..

Connecting to Manager at [host=rmpgf9-server0-data-platformengineering.eastus.cloudapp.azure.com, port=11099] ..

Successfully connected to: [host=rmpgf9-server0-data-platformengineering.eastus.cloudapp.azure.com, port=11099]

Cluster-1 gfsh>

List Gemfire Members
Cluster-1 gfsh>list members
         Name           | Id
----------------------- | ----------------------------------------------------------
rmpgf9-server0-locator  | 10.0.1.4(rmpgf9-server0-locator:2225:locator)<ec><v0>:1024
rmpgf9-server1-datanode | 10.0.1.5(rmpgf9-server1-datanode:2322)<v3>:10901

Cluster-1 gfsh>

Create a Gemfire region
gfsh>create region --name=accounts --type=REPLICATE
Member  | Status
------- | ---------------------------------------
server1 | Region "/accounts" created on "server1"

List Gemfire regions
gfsh>list regions
List of regions
---------------
accounts

Put to Gemfire regions
Cluster-1 gfsh>put --region=accounts --key="1234" --value="TestAccount"
Result      : true
Key Class   : java.lang.String
Key         : 1234
Value Class : java.lang.String
Old Value   : <NULL>

Cluster-1 gfsh>put --region=accounts --key="5678" --value="TestAccount2"
Result      : true
Key Class   : java.lang.String
Key         : 5678
Value Class : java.lang.String
Old Value   : <NULL>

Cluster-1 gfsh>

Describe Gemfire regions
Cluster-1 gfsh>describe region --name=accounts
..........................................................
Name            : accounts
Data Policy     : replicate
Hosting Members : rmpgf9-server1-datanode

Non-Default Attributes Shared By Hosting Members

 Type  |    Name     | Value
------ | ----------- | ---------------
Region | data-policy | REPLICATE
       | size        | 2
       | scope       | distributed-ack


Cluster-1 gfsh>

Show Gemfire metrics
Cluster-1 gfsh>show metrics

Cluster-wide Metrics

Category  |        Metric         | Value
--------- | --------------------- | -----
cluster   | totalHeapSize         | 4077
cache     | totalRegionEntryCount | 2
          | totalRegionCount      | 1
          | totalMissCount        | 1
          | totalHitCount         | 3
diskstore | totalDiskUsage        | 0
          | diskReadsRate         | 0
          | diskWritesRate        | 0
          | flushTimeAvgLatency   | 0
          | totalBackupInProgress | 0
query     | activeCQCount         | 0
          | queryRequestRate      | 0

Cluster-1 gfsh>

List Gemfire members
Cluster-1 gfsh>list members
         Name           | Id
----------------------- | ----------------------------------------------------------
rmpgf9-server0-locator  | 10.0.1.4(rmpgf9-server0-locator:2225:locator)<ec><v0>:1024
rmpgf9-server1-datanode | 10.0.1.5(rmpgf9-server1-datanode:2322)<v3>:10901

Cluster-1 gfsh>

Gemfire Pulse
GemFire Pulse is a Web Application that provides a graphical dashboard for monitoring vital, real-time health and performance of GemFire clusters, members, and regions.
Use Pulse to examine total memory, CPU, and disk space used by members, uptime statistics, client connections, WAN connections, and critical notifications. Pulse communicates with a GemFire JMX manager to provide a complete view of your GemFire deployment. You can drill down from a high-level cluster view to examine individual members and even regions within a member, to filter the type of information and level of detail.
By default, GemFire Pulse runs in an embedded container within a GemFire JMX manager node. You can optionally deploy Pulse to a Web application server of your choice, so that the tool runs independently of your GemFire clusters. Hosting Pulse on an application server also enables you to use SSL for accessing the application.
Launch Pulse from your web browser and login
http://rmpgf9-server0-data-platformengineering.eastus.cloudapp.azure.com:17070/pulse/login.html

Default User and PWD: admin/admin

