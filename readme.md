## Configuration du capteur de température

```bash
modprobe wire
modprobe w1-gpio
modprobe w1-therm
```

Ajouter à `/boot/firmware/config.txt` la ligne suivante :

```device_tree_overlay=overlays/w1-gpio.dtbo```

Rebooter le raspberry pi

## Modification des chemins 

Modifier les chemins vers le repertoire du code où nécessaire.

## Configuration des services 

```bash
# Copier dans /etc/systemd/system/server-cherry-py.service
# sudo systemctl daemon-reload
# sudo systemctl enable server-cherry-py
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
# sudo systemctl enable logtemp
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