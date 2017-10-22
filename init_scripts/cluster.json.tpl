{
    "global-properties":{
        "gemfire": "/usr/local/gemfire",
        "java-home" : "/usr/java/jdk1.8.0_144",
        "locators" : "{% for Server in Servers  if "Locator" in Server.Roles -%}{{ Server.PublicName }}[10000]{% if not loop.last -%},{%- endif %}{%- endfor %}",
        "cluster-home" : "/datadisks/disk1/gemfire_cluster",
        "classpath" : "{{ GemFireClassPath }}",
        "security-manager" : "io.pivotal.pde.gemfire.dynamic.security.DynamicSecurityManager",
        "security-peer-password" : "{{ GFPeerPassword }}",
        "security-admin-password" : "{{ GFAdminPassword }}",
        "security-disk-store-dir" : "/datadisks/disk1/gemfire_cluster/data/security",
        "distributed-system-id": 1
    },
   "locator-properties" : {
        "security-username": "gfpeer",
        "security-password" : "{{ GFPeerPassword }}",
        "port" : 10000,
        "jmx-manager-port" : 11099,
        "http-service-port" : 17070,
        "jmx-manager" : "true",
        "log-level" : "config",
        "statistic-sampling-enabled" : "true",
        "statistic-archive-file" : "locator.gfs",
        "log-file-size-limit" : "10",
        "log-disk-space-limit" : "100",
        "archive-file-size-limit" : "10",
        "archive-disk-space-limit" : "100",
        "enable-network-partition-detection" : "true",
        "jvm-options" : ["-Xmx2g","-Xms2g", "-XX:+UseConcMarkSweepGC", "-XX:+UseParNewGC" ]
    },
   "datanode-properties" : {
       "user": "gfpeer",
       "password" : "{{ GFPeerPassword }}",
        "conserve-sockets" : false,
        "log-level" : "config",
        "membership-port-range" : "10901-10999",
        "statistic-sampling-enabled" : "true",
        "statistic-archive-file" : "datanode.gfs",
        "log-file-size-limit" : "10",
        "log-disk-space-limit" : "100",
        "archive-file-size-limit" : "10",
        "archive-disk-space-limit" : "100",
        "tcp-port" : 10001,
        "server-port" : 10100,
        "gemfire.ALLOW_PERSISTENT_TRANSACTIONS" : "true",
        "locator-wait-time" : "300",
        "enable-network-partition-detection" : "true"
    },
    "hosts": {
    {% for Server in Servers if "DataNode" in Server.Roles or "Locator" in Server.Roles %}
        "{{ Server.Hostname }}" : {
            "host-properties" :  {
             },
             "processes" : {
               {% if "Locator" in Server.Roles  %}
                "{{ Server.Hostname }}-locator" : {
                    "type" : "locator",
                    "jmx-manager-hostname-for-clients" : "{{ Server.PublicName }}",
                    "jmx-manager-start" : "true"
                 }
               {% endif %}
               {% if "DataNode" in Server.Roles  %}
                "{{ Server.Hostname }}-datanode" : {
                    "type" : "datanode",
                    "jvm-options" : ["-Xmx{{ Server.XMX }}m","-Xms{{ Server.XMX }}m","-Xmn{{ Server.XMN }}m","-XX:+UseConcMarkSweepGC", "-XX:+UseParNewGC"]
                    {% if 'Rest' in Server.Roles %}
                    , "http-service-port": 18080,
                    "start-dev-rest-api" : "true"
                    {% endif %}
                 }
                {% endif %}
             }
        } {% if not loop.last -%},{%- endif %}
    {% endfor %}
   }
}
