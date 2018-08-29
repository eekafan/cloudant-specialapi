echo ''
echo 'DELETE any testviewdb via api - expect pass'
echo ''
curl --insecure -u $1:$2 $3/_api/managedb/testviewdb100000 -X DELETE
echo ''
echo 'CREATE testviewdb via api - expect pass'
echo ''
curl --insecure -u $1:$2 $3/_api/managedb/testviewdb100000 -X PUT
echo ''
echo 'SUBMIT CREATE two new views via api - pass'
echo ''
curl --insecure -u $1:$2 $3/_api/migrate/testviewdb100000/_design/pmkctest1 -X PUT -d @testview/pmkc2.json 
echo ''
curl --insecure -u $1:$2 $3/_api/migrate/testviewdb100000/_design/pmkctest2 -X PUT -d @testview/pmkc2.json 
echo ''
echo 'SUBMIT UPDATE existing view vai api - pass'
echo ''
curl --insecure -u $1:$2 $3/_api/migrate/testviewdb100000/_design/pmkctest2 -X PUT -d @testview/pmkc4.json 
echo ''
echo 'sleeping 120 seconds to allow jobs to be serviced before deletion attempt'
sleep 120
echo ''
echo 'SUBMIT DELETE existing view  via api - expect pass'
echo ''
curl --insecure -u $1:$2 $3/_api/migrate/testviewdb100000/_design/pmkctest2 -X DELETE 
