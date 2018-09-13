# Installing the specialapi

The specialapi is most conveniently installed on the two load balancers of a cloudant local cluster.  

The existing virtualip mechanism for the cloudant cluster is used to provide a highly-available service for this specialapi.

The specialapi is designed for use in RHEL7 or Centos7 hosted cloudant cluster environments. 
  
A new install requires several steps: 
  
* installing (python-based) flask webserver on load balancers
* configuring existing load-balancer haproxys to redirect \_api endpoint requests to flask
* editing the specialapi configuration files  
* installing the specialapi software (flask-served content)

With a patch install, only the last step is necessary.

_Optionally, the specialapi can be used as a front-end for api-based requests to the cloudant-performancecollector tool. This capability requires the cloudant-performancecollector to be installed and running._

You can test the api at any time with the supplied test scripts. See the `Testing` documentation for this API.


##	Flask Server libraries
As user 'root', on each load-balancer, install python libraries for the flask server and its connections via the api :  
  
```
$ pip install flask
$ pip install requests  
```  
## 	Configuring haproxy for Flask (_api) backend

These instructions assume that a working cloudant cluster via primary-secondary load-balancer pair is in operation. The steps require incremental changes to the standard Cloudant Local installation.

The \_api endpoint backend is configured to point to localhost:5000 when the api is run on each load-balancer.

lines are added after the dashboard setup. They follow a similar pattern to the dashboard setup. 

1)	Add acl for api_assets after dashboard_assets
    
```  
acl dashboard_assets path_beg /dashboard.     
acl api_assets path_beg /_api
```  

2)	Add use\_backend for api\_assets\_host after dashboard\_assets\_host

```  
use_backend dashboard_assets_host if dashboard_assets      
use_backend api_assets_host if api_assets  
```  

3)	Add backend api\_assets\_host after 'backend dashboard\_assets\_host'  

```
backend api_assets_host 
  option httpchk GET /_api    
  server localhost 127.0.0.1:5000 check inter 7s   
```  

Restart the load balancer (cast node restart) after the change to the haproxy.cfg file.

The /var/log/haproxy.log file will show failures for this backend until the specialapi services are configured and running.

##	Installing the specialapi software

### Collecting software from Github

cloudant-specialapi is released via github. Use a github client to download the release level required.

The github repository is 
`https://github.com/rombachuk/cloudant-specialapi`

The releases option in Github shows the available releases.
Download from the site in either tar.gz or zip format, and place in a suitable directory, as `root` on the load-balancer eg `/root/software`


### 	Unpacking 
Then unpack the software with `tar xvf` or `unzip`, depending on the download format from github.

The software unpacks to the following directories :  
  
  * cloudant-specialapi (the software to be installed)
  * documentation (markdown files documenting the package)
  * test (testing scripts for the package)
  * deploy (installation & patch scripts for the package)

#### Example

Software release 27.0.2 is downloaded to server cl11c74lb1 directory  `/root/software/cloudant-specialapi-27.0.2.tar.gz` and unpacked with tar as  
  
  
```  
[root@cl11c74lb1 cloudant-specialapi-27.0.2]# pwd
/root/software/cloudant-specialapi-27.0.2
[root@cl11c74lb1 cloudant-specialapi-27.0.2]# ls -l
total 4
drwxrwxr-x 2 root root 275 Aug 29 17:44 cloudant-specialapi
drwxrwxr-x 2 root root  54 Aug 29 17:44 deploy
drwxrwxr-x 2 root root 280 Aug 29 17:44 documentation
-rw-rw-r-- 1 root root  83 Aug 29 17:44 README.md
drwxrwxr-x 5 root root 300 Aug 29 17:44 test
```    

### Clean Install
This option is used when a brand new install is required, or when an existing install is to be deleted and reset.

Three steps are needed :  
  
* configure cluster access and enable api features in cloudant-specialapi/csapi.conf
* enable usernames to use the api in cloudant-specialapi/csapi_users
* run the deploy/clean_install.sh script


Do the installation as `root`

#### Configuration (csapi.conf)

The API can be configured to enable certain features.  
If the feature is disabled, then all api calls to that endpoint will fail. The features are enabled by api admin teams in the csapi.conf file
  
```
clusterurl      http://activesn.bkp.ibm.com  
admincredentials    bWlk********3MHJk    
migrateapi_status   enabled   
managedbapi_status  enabled   
perfagentapi_status enabled
```   
* The clusterurl should be the vip of your cloudant local cluster.  
* The admin credentials shoud be a base64encoding of the string `user:password` where the user is a cluster admin user.  
* migrateapi_status enabled for view and index operations
* managedbapi_status enabled for database operations
* perfagentapi_status enabled for cloudant-performancecollector calls via this api _(cloudant-performancecollector must already be operational)_

You can disable features at any later time by setting them `disabled` and restarting the `csapi` service.

#### Configuration (csapi_users)

The API elevates standard user capability to that of admin for the request made. As as example, a standard user could create a database.

Only password-correct requests from those users listed in csapi_users are accepted.  

In the following example, only three users can use the API :  

```  
[root@cl11c74lb1 cloudant-specialapi]# cat csapi_users
northamd
middleamd
northa  
```  

#### Installation

Once the configuration steps are done, go to `deploy` directory, and run `./clean_install.sh` 
  
This script will :  

* create a new installation in `/opt/cloudant-specialapi`
* backup any pre-existing `/opt/cloudant-specialapi` content to a new directory `opt/cloudant-specialapi-bkp-YYYYMMDDHHmm` where YYYYMMDDHHmm is the datetime of run of the install. You can delete this backup once you are happy with the running of the new installation
* create new service files in `/etc/init.d` and start them : services are created called `csapi`, `csapi-migrater`
* backup any pre-existing service files in `/etc/init.d` for those services within `opt/cloudant-specialapi-bkp-YYYYMMDDHHmm/init.d`. You can delete this backup once you are happy with the running of the new installation

#### Patch Install
This option is used when an upgrade to an existing installation is required. No changes to the csapi.conf is carried out, so cluster url and credentials are left as they are.

Do the installation as `root`

Go to `deploy` directory, and run `./patch_install.sh` 

This script will :  
  
* update the *.py files in `/opt/cloudant-specialapi`
* backup any pre-existing `/opt/cloudant-specialapi` content to a new directory `opt/cloudant-specialapi-bkp-YYYYMMDDHHmm` where YYYYMMDDHHmm is the datetime of run of the install. You can delete this backup once you are happy with the running of the patched installation
* create new service files in `/etc/init.d` and start them : services are created called `csapi`, `csapi-migrater`
* backup any pre-existing service files in `/etc/init.d` for those services within `opt/cloudant-specialapi-bkp-YYYYMMDDHHmm/init.d`. You can delete this backup once you are happy with the running of the new installation






