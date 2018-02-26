[Unit]
Description=GemFire Cluster
After=remote-fs.target systemd-journald-dev-log.socket network-online.target
Wants=network-online.target

[Install]
WantedBy=multi-user.target

[Service]
Type=forking
Restart=no
TimeoutSec=5min
KillMode=control-group
User={{ RunAsUser }}
Group={{ RunAsUser }}
WorkingDirectory=/datadisks/disk1/gemfire_cluster
ExecStart=/usr/bin/python cluster.py start
ExecStop=/usr/bin/python cluster.py stop
