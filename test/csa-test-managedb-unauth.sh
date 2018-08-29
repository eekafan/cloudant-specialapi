echo 'READ db - fail unauthorised'
curl --insecure -u $1:$2 $3/metrics 
echo ' '
echo 'CREATE db - fail unauthorised'
curl --insecure -u $1:$2 $3/newdb1000000 -X PUT
echo ' '
echo 'DELETE db - fail unauthorised'
curl --insecure -u $1:$2 $3/stats -X DELETE
echo ' '

