#!/bin/bash
if [[ -z $1 ]]; then
 read -p 'Username: ' user 
else
 user=$1
fi
if [[ -z $2 ]]; then
 read -sp 'Password: ' password 
else
 password=$2
fi
echo ''
if [[ -z $3 ]]; then
 read -p 'Cluster URL (including http(s)): ' url 
else
 url=$3
fi

epoch=`date +%Y%m%d%H%M%S`
echo 'running managedb tests'
./csa-test-managedb-unauth.sh $user $password $url > ./resultlog/csa-managedb-unauth.log
./csa-test-managedb-pass.sh $user $password $url > ./resultlog/csa-managedb-pass.log
echo 'running migrate-view tests'
./csa-test-migrate-view-pass.sh $user $password $url > ./resultlog/csa-migrate-view-pass.log
./csa-test-migrate-view-unauth.sh $user $password $url > ./resultlog/csa-migrate-view-unauth.log
echo 'running migrate-index tests'
./csa-test-migrate-index-pass.sh $user $password $url > ./resultlog/csa-migrate-index-pass.log
./csa-test-migrate-index-unauth.sh $user $password $url > ./resultlog/csa-migrate-index-unauth.log
echo 'sleeping 60 seconds and then collecting logs in case problems with jobs'
sleep 60
tail -n 100 /var/log/migrateworker.log > ./resultlog/csa-migrate-worker.log
tar czvf resultlog/resultlog-$epoch.tar resultlog/*.log
