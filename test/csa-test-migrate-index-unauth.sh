echo 'CREATE two index direct - expect fail'
echo ''
curl --insecure -u $1:$2 $3/testindexdb100000/_index -H 'Content-Type:application/json' -X POST -d @testindex/idx1.json
echo ''
echo 'DELETE existing index direct - expect fail - cluster always returns ok so use list to check'
echo ''
curl --insecure -u $1:$2 $3/testindexdb100000/_index/_design/potilaanSyntymaAika3/json/potilaanSyntymaAika-index3 -X DELETE 
echo ''
echo 'LIST all index in testindexdb direct check index3 still exists'
echo ''
curl --insecure -u $1:$2 $3/testindexdb100000/_index
