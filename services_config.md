```bash
# Copier dans /etc/systemd/system/server-cherry-py.service
# sudo systemctl daemon-reload
# sudo service server-cherry-py start
[Unit]
Description=Regular temperature log to csv file

[Service]
Type=simple
Restart=always
RestartSec=10
User=pi
ExecStart=/usr/bin/python3 -u /home/cedric/dev/pileds/logTemp.py
WorkingDirectory=/home/cedric/dev/pileds/
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
```

```bash
# Copier dans /etc/systemd/system/logtemp.service
# sudo systemctl daemon-reload
# sudo service logtemp start
[Unit]
Description=Regular temperature log to csv file

[Service]
Type=simple
Restart=always
RestartSec=10
User=pi
ExecStart=/usr/bin/python3 -u /home/cedric/dev/pileds/logTemp.py
WorkingDirectory=/home/cedric/dev/pileds/
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target```