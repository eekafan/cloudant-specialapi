echo ''
echo 'DELETE any testindexdb via api - expect pass'
echo ''
curl --insecure -u $1:$2 $3/_api/managedb/testindexdb100000 -X DELETE
echo ''
echo 'CREATE testindexdb via api - expect pass'
echo ''
curl --insecure -u $1:$2 $3/_api/managedb/testindexdb100000 -X PUT
echo ''
echo 'SUBMIT CREATE two index via api - pass'
echo ''
curl --insecure -u $1:$2 $3/_api/migrate/testindexdb100000/_index -X POST -d @testindex/idx1.json
curl --insecure -u $1:$2 $3/_api/migrate/testindexdb100000/_index -X POST -d @testindex/idx2.json
echo ''
echo 'sleeping 20 seconds to allow jobs to be serviced before list attempt'
sleep 20
echo ''
echo 'LIST all index in testindexdb direct ie not via api - pass'
echo ''
curl --insecure -u $1:$2 $3/testindexdb100000/_index 
echo ''
echo 'SUBMIT DELETE existing index  via api - expect pass'
echo ''
curl --insecure -u $1:$2 $3/_api/migrate/testindexdb100000/_index/_design/potilaanSyntymaAika/json/potilaanSyntymaAika-index -X DELETE 
