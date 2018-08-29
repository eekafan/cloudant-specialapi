#!/bin/bash
now=`date +%Y%m%d%H%M`
systemctl stop csapi
systemctl stop csapi_migrater
systemctl stop csapi_perfagent_processor
cp -r /opt/cloudant-specialapi /opt/cloudant-specialapi-bkp-$now
mkdir /opt/cloudant-specialapi-bkp-$now/init.d
cp /etc/init.d/csapi /opt/cloudant-specialapi-bkp-$now/init.d
cp /etc/init.d/csapi_migrater /opt/cloudant-specialapi-bkp-$now/init.d
cp /etc/init.d/csapi_perfagent_processor /opt/cloudant-specialapi-bkp-$now/init.d
rm -rf /opt/cloudant-specialapi
rm -f /etc/init.d/csapi /etc/init.d/csapi_migrater /etc/init.d/csapi_perfagent_processor
cp -r ../cloudant-specialapi /opt
cp /opt/cloudant-specialapi/csapi /etc/init.d
cp /opt/cloudant-specialapi/csapi_migrater /etc/init.d
systemctl enable csapi
systemctl enable csapi_migrater
systemctl start csapi
systemctl start csapi_migrater