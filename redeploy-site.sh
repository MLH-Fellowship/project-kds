#!/bin/bash

#cd into project portfolio
cd /root/portfolio-site

#make sure to get latest github repo version
git fetch && git reset origin/main --hard

#kill the old virtual env
rm -rf python3-virtualenv

#makes the virtual env
python3 -m venv python3-virtualenv
#activate the virtual env
source python3-virtualenv/bin/activate

#make sure pip is latest update
pip install --upgrade pip
#make sure to install pip's requirements
pip install -r requirements.txt

#restarts the service from /etc/systemd/system/myportfolio.service
systemctl restart myportfolio

#note: if make changes to the myportfolio.service file, then need to run the following cmd
# systemctl daemon-reload

#note: run the following cmd to check the status of the systemd service
# systemctl status myportfolio