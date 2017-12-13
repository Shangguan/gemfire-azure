******************************************************************************************************
Use the following steps to validate your Azure GemFire deployment.  This is also a good way to get
familiar with some of the gfsh cli commands.  Sample output is included.

To learn more about GemFire and the cli (gfsh), please reference the following url:
   http://gemfire.docs.pivotal.io/gemfire/about_gemfire.html
******************************************************************************************************
START: Validate GemFire 
   NOTE1: Find your DNS names and IP addresses by looking at /etc/hosts (cat /etc/hosts)
   NOTE2: Replace the DNS names in the following examples with your actual DNS names
   NOTE3: The last section discusses the Web Interface Pulse, and shows how to launch it and login
   NOTE4: Run the commands as user gfadmin
******************************************************************************************************
STEP 1 - create a scratch directory and cd to it
gfsh saves locator and server working directories and log files in this location
   cd ~
   mkdir my_gemfire
   cd my_gemfire/
******************************************************************************************************
STEP 2 - Start gfsh by running gfsh at the command prompt
   gfsh
    _________________________     __
   / _____/ ______/ ______/ /____/ /
  / /  __/ /___  /_____  / _____  /
 / /__/ / ____/  _____/ / /    / /
/______/_/      /______/_/    /_/    9.1.1

Monitor and Manage Pivotal GemFire
******************************************************************************************************
STEP 3 - Connect to a GemFire locator
   gfsh>connect --locator=rmpgf9-server0.eastus.cloudapp.azure.com[10334]
   
   Connecting to Locator at [host=rmpgf9-server0.eastus.cloudapp.azure.com, port=10334]
   Connecting to Manager at [host=rmpgf9-server0.eastus.cloudapp.azure.com, port=1099]
   Successfully connected to: [host=rmpgf9-server0.eastus.cloudapp.azure.com, port=1099]
******************************************************************************************************
STEP 4 - List GemFire Members
   Cluster-1 gfsh>list members
            Name           | Id
   ----------------------- | ----------------------------------------------------------
   rmpgf9-server0-locator  | 10.0.1.4(rmpgf9-server0-locator:2225:locator)<ec><v0>:1024
   rmpgf9-server1-datanode | 10.0.1.5(rmpgf9-server1-datanode:2322)<v3>:10901
******************************************************************************************************
STEP 5 - Create a GemFire region
   gfsh>create region --name=accounts --type=REPLICATE
   Member  | Status
   ------- | ---------------------------------------
   server1 | Region "/accounts" created on "server1"
******************************************************************************************************
STEP 6 - List GemFire regions
   gfsh>list regions
   List of regions
   ---------------
   accounts
******************************************************************************************************
STEP 7 - Use the put command to add an entry in the region
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
******************************************************************************************************
STEP 8 - Describe GemFire regions
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
******************************************************************************************************
STEP 9 - Show GemFire metrics
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
******************************************************************************************************
STEP 10 - List GemFire members
   Cluster-1 gfsh>list members
            Name           | Id
   ----------------------- | ----------------------------------------------------------
   rmpgf9-server0-locator  | 10.0.1.4(rmpgf9-server0-locator:2225:locator)<ec><v0>:1024
   rmpgf9-server1-datanode | 10.0.1.5(rmpgf9-server1-datanode:2322)<v3>:10901
******************************************************************************************************
GemFire PULSE
   GemFire Pulse is a Web Application that provides a graphical dashboard for monitoring vital, 
   real-time health and performance of GemFire clusters, members, and regions.  To learn more about 
   Pulse, please reference the following url:
      http://gemfire.docs.pivotal.io/geode/tools_modules/pulse/pulse-overview.html

   Launch Pulse from your web browser and login using the DNS name of your VM. For example:
      http://rmpgf9-server0.eastus.cloudapp.azure.com:7070/pulse/login.html
      Default UserID/PWD: admin/admin
******************************************************************************************************
