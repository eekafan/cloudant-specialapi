# Configuring the API
## Enabling the API
The special api can be disabled by stopping the service.
You can test if the api is available by checking the _api endpoint.
eg  
  
```  
curl http://activesn.bkp.ibm.com/_api  
   
{
  "cloudant special api": "Welcome",
  "version": "1.0.0"
} 
```    
  
You will see a 503 error if it is unavailable  
  
``` 
curl http://activesn/_api   
<html><body><h1>503 Service Unavailable</h1>
No server is available to handle this request.
</body></html>  
```  
  
##	Enabling features
The API can be configured to enable features or not
If the feature is disabled, then all api calls to that endpoint will fail.
The features are enabled by api admin teams in the csapi.conf file  
  
```
clusterurl		http://activesn.bkp.ibm.com  
admincredentials	bWlk********3MHJk    
migrateapi_status	enabled   
managedbapi_status	enabled   
perfagentapi_status	enabled  
```
  
Any value other than 'enabled' disables the specific feature.

##	Allowing access
The API can be configured to allow specific users the right to use it. Correct credentials must also be supplied in the call.
The valid list of users is listed in csapi_users.

##	API worker configuration
The perfagent api runs a worker
