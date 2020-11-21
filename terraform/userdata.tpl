#!/bin/bash

sudo apt-get -y update
sudo apt-get -y install python3-venv
sudo apt-get -y install python3-pip
cd /home/ubuntu

sudo su - ubuntu -c "git clone https://github.com/mEyob/used-car-analytics"
sudo su - ubuntu -c "cd used-car-analytics"
sudo su - ubuntu -c "chmod 700 run.sh"
sudo su - ubuntu -c "python3 -m venv python-env"
sudo su - ubuntu -c "source python-env/bin/activate"
sudo su - ubuntu -c "pip install -r requirements.txt"

# add crontab to perform scrapping at every bootup
sudo su - ubuntu -c "crontab -l > /tmp/mycrontab"
sudo su - ubuntu -c "echo '@reboot               /home/ubuntu/used-car-analytics/run.sh &' >> /tmp/mycrontab"
sudo su - ubuntu -c "crontab /tmp/mycrontab"
