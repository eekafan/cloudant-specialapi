# Introduction
## Release Information
This document version is aligned with Release 27.0.3
## Document Purpose
The purpose of this document is to provide a user guide for the cloudant-specialapi tool, delivered by IBM Services. 
The tool is provided on an opensource basis, and customers are free to enhance or modify the tool in any way. Such changes may of course modify the features, options, and descriptions provided in this document.
## Intended Audience 
The intended audience for this document are IBM customers who are deploying Cloudant Local Edition Clusters, and wish to use the specialapi features in the management of operations on their clusters.
## Commercial Clarification 
 
This document does not amend in any way existing agreed terms and conditions of service, and readers are referred to IBM client representatives for any issues concerning terms and condition of service.
## Notices 
INTERNATIONAL BUSINESS MACHINES CORPORATION PROVIDES THIS PUBLICATION "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. Some jurisdictions do not allow disclaimer of express or implied warranties in certain transactions, therefore, this statement may not apply to you.
This information could include technical inaccuracies or typographical errors. Changes are periodically made to the information herein; these changes will be incorporated in new editions of the publication. IBM may make improvements and/or changes in the product(s) and/or the program(s) described in this publication at any time without notice.
Any references in this information to non-IBM websites are provided for convenience only and do not in any manner serve as an endorsement of those websites. The materials at those websites are not part of the materials for this IBM product and use of those websites is at your own risk.
IBM may use or distribute any of the information you provide in any way it believes appropriate without incurring any obligation to you.
IBM, the IBM logo, and ibm.com are trademarks or registered trademarks of International Business Machines Corp., registered in many jurisdictions worldwide. Other product and service names might be trademarks of IBM or other companies. A current list of IBM trademarks is available on the web at Copyright and trademark information  

#	Features Summary
##	Database Operations (_api/managedb)
This feature is intended to allow temporary 'elevated' privileges for database level operations. This allows users to create and delete databases, but without being granted '_admin' and 'server_admin' privilege. As a result, users can be prevented from seeing database content for sets of databases on a cluster that they share with other users.  
  
The managedb component supports:  
  
* creation of database
* deletion of database
* reading database endpoint  
  
for users who do not have '_admin' and 'server_admin' privilege on the cluster.  

The user makes REST calls to the cluster _api/managedb endpoint to achieve these operations.
Only those users listed in csapi_users file will be authorised.  
  
The REST call can use either a AuthSession cookie, or basic authentication.
  
The API will test the credentials supplied in the REST call against the cluster cluster-port authentication scheme. Invalid credentials at point of test will mean the call is rejected.  
  
Databases are created with members.names = request-username so that the database is read-write to the requesting user, and not world-open to anonymous requests.
## Design Document Operations via Operational Queue (_api/migrate)
This feature is intended to ensure create, update and delete operations on design-documents are processed as an operational queue rather than in parallel.  

This limits the index\_create, index\_update, view\_create, view\_update and view\_compact volumes on the cluster.   
  
For view updates, the 'move and shift' technique is used, which ensures that reads with update=true or stale=false (default settings) will not block during the update process.  

The migrate component supports:  
  
* submission of create/update job (view or index) to the queue, returning jobid, if accepted
* submission of delete job (view or index) to the queue, returning jobid if accepted
* reading status of job, using a jobid
* deletion of designdocument (view or index type)
  
The feature can be used by users who do not have 'admin' privilege to a database they are submitting the job for. The api temporarily elevates their privilege.  

This allows the blocking of design-doc operations via the direct Cloudant api, preventing cluster overload through high numbers of parallel view updates.  
  
The user makes REST calls to the cluster _api/migrate endpoint to achieve these operations.  

Only those users listed in csapi_users file will be authorised.  
  
The REST call can use either a AuthSession cookie, or basic authentication.  

The API will test the credentials supplied in the REST call against the cluster cluster-port authentication scheme. Invalid credentials at point of test will mean the call is rejected.  

## Performance Metrics Collection via Operational Queue (_api/perfagent)
This feature is intended to allow interaction with the cloudant-performancecollector tool using an api call :   

* The api is used to submit a job which is serviced by the cloudant-performancecollector tool. 
* The api tests the credentials supplied in the job submission  REST call. Invalid credentials will mean the call is rejected and the job is not submitted.
* The cloudant-performancecollector services one job at a time to limit the cpu usage overhead of performance collection and processing.
* The results are placed in JSON format by the performancecollector into the job document which can be read via the api. The job is marked completed once the results are placed. 


The results provide:  

* cluster performance metrics broken down by resource level and time-period. 
* statistics at a finer scope than available from the metrics database  
* breakdown of traffic and performance response rates by database-sets _which may reflect different users/projects/tasks sharing the same cluster_  

Resource levels supported are:  
  
* all (ie whole cluster)
* database
* database + verb (ie reads, writes, deletes, etc)
* database,verb,endpoint  
_where **endpoint** reflects grouping of requests to endpoint type_  
-- \_design (ddl operations)   
-- 	\_find (all cloudantquery type calls)  
--	design/view (all map-reduce calls)  
--	documentlevel (all calls to individual docs  
  
Time-Period granularity levels supported for the supplied start- and end- datetime are:  
  
* per-minute, per-hour, per-day, all (the whole report-period)  
  

    
Defaults are applied if parameters are omitted in the request. These are set in a configuration file **cloudant-specialapi/perfagent.conf** by the specialapi operator (typically the cluster dba team).  

The cloudant-performancecollector supports a wide range of options which include data exclusion lists and threshold detection. The cloudant-performancecollector documentation should be consulted for a full view of all the options available.
  
Only those users listed in csapi_users file will be authorised.
The REST call can use either a AuthSession cookie, or basic authentication.  


