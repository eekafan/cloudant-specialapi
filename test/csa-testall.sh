epoch=`date +%s`
./csa-test-managedb-unauth.sh $1 $2 $3 > ./resultlog/csa-managedb-unauth.log
./csa-test-managedb-pass.sh $1 $2 $3 > ./resultlog/csa-managedb-pass.log
./csa-test-migrate-view-unauth.sh $1 $2 $3 > ./resultlog/csa-migrate-view-unauth.log
./csa-test-migrate-view-pass.sh $1 $2 $3 > ./resultlog/csa-migrate-view-pass.log
./csa-test-migrate-index-unauth.sh $1 $2 $3 > ./resultlog/csa-migrate-index-unauth.log
./csa-test-migrate-index-pass.sh $1 $2 $3 > ./resultlog/csa-migrate-index-pass.log
echo 'sleeping 60 seconds and then collecting logs in case problems with jobs'
sleep 60
tail -n 100 /var/log/migrateworker.log > ./resultlog/csa-migrate-worker.log
tar czvf resultlog/resultlog-$epoch.tar resultlog/*.log
