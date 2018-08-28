echo ''
echo 'READ db via api - pass'
echo ''
curl --insecure -u $1:$2 $3/_api/managedb/metrics
echo ''
echo 'CREATE db via api - expect pass'
echo ''
curl --insecure -u $1:$2 $3/_api/managedb/newdb1000000 -X PUT
echo ''
echo 'READ newly created db via api - expect pass'
echo ''
curl --insecure -u $1:$2 $3/_api/managedb/newdb1000000
echo ''
echo 'DELETE db via api - expect pass'
curl --insecure -u $1:$2 $3/_api/managedb/newdb1000000 -X DELETE
echo ''