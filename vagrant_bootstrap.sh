#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip
apt-get install -y git
apt-get install -y python-dev
apt-get install -y vim
pip install virtualenv
virtualenv /vagrant/example/env
source /vagrant/example/env/bin/activate
pip install -r /vagrant/example/requirements.txt
python /vagrant/example/manage.py syncdb

