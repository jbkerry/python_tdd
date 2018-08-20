Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.6
* virtualenv + pip
* Git

e.g., on Ubuntu:

  sudo add-apt-repository ppa:fkrull/deadsnakes
  sudo apt-get install nginx git python3.6 python3.6-venv

## Nginx Virual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME with, e.g., staging.my-domain.com
* replace SOMESECRET with email password

## Folder structure
Assume we have a user account at /home/username

/home/username
|_ sites
   |_ SITENAME
       |-- database
       |-- source
       |-- static
       |-- virtualenv
