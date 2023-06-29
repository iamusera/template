#!/bin/bash

source ~/.bash_profile

start_server(){
  unzip /app/appdata/care-modle.zip -d /app/appdata/care_modle
  unzip /app/appdata/py36-package.zip -d /app/appdata/sit-packages
  python3 -m pip install --no-index --find-links=/app/appdata/sit-packages/ -r /app/appdata/care_modle/requirements.txt
  supervisord -c /app/appdata/care_modle/deploy/supervisor.conf
}

restart_server(){
  supervisorctl -c /app/appdata/care_modle/deploy/supervisor.conf restart care_modle
}

pid=`ps -ef|grep supervisor |awk 'NR>=2{print $2}'`   
if [ -z "${pid}" ]; then
  printf "###### start server ###### \n"
  start_server
else
  printf "###### restart server ######\n"
  restart_server
fi