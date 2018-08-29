echo 'CREATE new view direct - expect fail'
echo ''
curl --insecure -u $1:$2 $3/testviewdb100000/_design/pmkctest2 -X PUT -d @testview/pmkc2.json 
echo ''
echo 'UPDATE existing view direct - expect fail'
echo ''
curl --insecure -u $1:$2 $3/testviewdb100000/_design/pmkctest1 -X PUT -d @testview/pmkc2.json 
echo ''
