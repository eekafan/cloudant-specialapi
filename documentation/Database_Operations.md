#	Database Operations (_api/managedb)
## Overview
The user or application submits a REST call to the api and can:  
  
* add a new database with a PUT, setting permissions so that requester has read-write access  
* delete a database with a DELETE  
* read database info with a GET  
  
## 	Examples
###	Creates

Failed request without using the api (user does not have permission)

```  
curl -u northamd:*** http://activesn.bkp.ibm.com/newdb100 -X PUT  
  
{"error":"forbidden","reason":"server_admin access is required for this request"}  
```
  
Successful request using the api  
  
``` 
curl -u northamd:*** http://activesn.bkp.ibm.com/_api/managedb/newdb100 -X PUT
     
{
  "result": "ok"
}  
```

###	Reads
reads any database since run as server_admin user : even ones which are normally not available  
  
```
curl -u northamd:*** http://activesn.bkp.ibm.com/_api/managedb/newdb100  
  
{"update_seq": "8-g1AAAAGzeJzLYWBg4MhgTmGQTc7JL01JzCtxSEwuySxLLc7TS8ou0MtMytVLzs_ 
NASpjSmRIkv___39WIiORGpIUgGSSPWl6HEB64knTkwDSU0-SnjwWIMnQAKSA2uaTqm8BRN9-UvUdgOi7T6q-BxB9IP9lAQClDJI2",  
 "disk_size": 66808, "sizes": {"active": 0, "external": 0, "file": 66808},  
 "purge_seq": 0, "doc_count": 0, "compact_running": false, "db_name": "newdb100",  
"data_size": 0, "doc_del_count": 0, "instance_start_time": "0",   
"other": {"data_size": 0}, "disk_format_version": 6}  
```
### Deletes
Failed request without using the api (user does not have permission)
  
```
curl -u northamd:*** http://activesn.bkp.ibm.com/newdb100 -X DELETE
 
{"error":"unauthorized","reason":"You are not a server admin."}. 
```
Successful request using the api 
   
```   
curl -u northamd:*** http://activesn.bkp.ibm.com/_api/managedb/newdb100 -X DELETE  
   
{"ok": true}
```	

 
