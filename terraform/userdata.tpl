#!/bin/bash
appHome=/home/ubuntu
sudo apt-get -y update
sudo apt-get -y install python3-venv
sudo apt-get -y install python3-pip
cd $appHome

sudo su - ubuntu -c "git clone https://github.com/mEyob/used-car-analytics"
chmod 700 $appHome/used-car-analytics/run.sh
python3 -m venv $appHome/python-env
source $appHome/python-env/bin/activate
pip3 install -r $appHome/used-car-analytics/requirements.txt

# add crontab to perform scrapping at every bootup
sudo su - ubuntu -c "crontab -l > /tmp/mycrontab"
sudo su - ubuntu -c "echo '@reboot               $appHome/used-car-analytics/run.sh &' >> /tmp/mycrontab"
sudo su - ubuntu -c "crontab /tmp/mycrontab"
