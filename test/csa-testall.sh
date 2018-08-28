./cmc-test-managedb-unauth.sh $1 $2 $3 > cmc-managedb-unauth.log
./cmc-test-managedb-pass.sh $1 $2 $3 > cmc-managedb-pass.log
./cmc-test-migrate-view-unauth.sh $1 $2 $3 > cmc-migrate-view-unauth.log
./cmc-test-migrate-view-pass.sh $1 $2 $3 > cmc-migrate-view-pass.log
./cmc-test-migrate-index-unauth.sh $1 $2 $3 > cmc-migrate-index-unauth.log
./cmc-test-migrate-index-pass.sh $1 $2 $3 > cmc-migrate-index-pass.log