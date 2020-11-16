#!/bin/bash

sudo apt-get -y update
sudo apt-get -y install python3-venv
cd $HOME
git clone https://github.com/mEyob/used-car-analytics
cd used-car-analytics
chmod 700 run.sh
python3 -m venv python-env
source python-env/bin/activate
pip install -r requirements.txt
./run.sh

# add crontab to perform scrapping at every bootup
crontab -l > /tmp/mycrontab
echo '@reboot               /home/ubuntu/used-car-analytics/run.sh &' >> /tmp/mycrontab
crontab /tmp/mycrontab