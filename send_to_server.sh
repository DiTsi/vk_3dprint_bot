#!/bin/bash
IP=<server_ip>

scp ./bot.py					iziprint@$IP:/home/iziprint/
scp ./config_parser.py			iziprint@$IP:/home/iziprint/
scp ./export_pip_packages.sh	iziprint@$IP:/home/iziprint/
scp ./notifier.py				iziprint@$IP:/home/iziprint/
scp ./requirements.txt			iziprint@$IP:/home/iziprint/
scp ./strings.ini				iziprint@$IP:/home/iziprint/
scp ./volume.py					iziprint@$IP:/home/iziprint/
exit 0
