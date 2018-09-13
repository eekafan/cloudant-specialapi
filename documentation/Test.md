# Testing the specialapi

The specialapi can be tested from one of the loadbalancers with the scripts delivered with the release.  
They are located in the `test` directory of the deliverable from github.

The master test script expects a username/password and clusterurl from the invoker. These can be supplied as parameters or on the command line.  
The username should be a standard user, who gains elevated privileges by using the api.

The master script calls a set of slave scripts which have expected outcomes. 

The scripts use `curl` to test the api.

The results are placed in a tarball in the `test/resultlog` directory. This tarball can be inspected or sent to the specialapi support team at `email: andrew.rombach@uk.ibm.com`.


##	Example test run
  
The script should be invoked as user `root`.   
The username supplied should be an non-admin user, with presence in the csapi_users file.  
If an admin user is supplied, some of the 'expected-fail' tests will pass.

The script takes about 3-4 minutes to run.

This is an example dialogue   
  
```
[root@cl11c74lb1 test]# ./csa-testall.sh
Username: northamd
Password:
Cluster URL (including http(s)): https://cl11c74vip.ibm.com
running managedb tests
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   107    0   107    0     0   1493      0 --:--:-- --:--:-- --:--:--  1507
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   107    0   107    0     0   2611      0 --:--:-- --:--:-- --:--:--  2675
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   107    0   107    0     0   2766      0 --:--:-- --:--:-- --:--:--  2815
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    35  100    35    0     0    807      0 --:--:-- --:--:-- --:--:--   813
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    35  100    35    0     0    893      0 --:--:-- --:--:-- --:--:--   897
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    35  100    35    0     0    790      0 --:--:-- --:--:-- --:--:--   795
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    35  100    35    0     0    832      0 --:--:-- --:--:-- --:--:--   853
running migrate-view tests
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    35  100    35    0     0    819      0 --:--:-- --:--:-- --:--:--   833
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    35  100    35    0     0    761      0 --:--:-- --:--:-- --:--:--   777
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   725  100    35  100   690    690  13607 --:--:-- --:--:-- --:--:-- 13800
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   725  100    35  100   690    806  15892 --:--:-- --:--:-- --:--:-- 16046
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   737  100    35  100   702    748  15019 --:--:-- --:--:-- --:--:-- 15260
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    35  100    35    0     0    428      0 --:--:-- --:--:-- --:--:--   432
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   797    0   107  100   690   1907  12297 --:--:-- --:--:-- --:--:-- 12545
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   797    0   107  100   690   1755  11318 --:--:-- --:--:-- --:--:-- 11500
running migrate-index tests
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    35  100    35    0     0    585      0 --:--:-- --:--:-- --:--:--   593
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    35  100    35    0     0    607      0 --:--:-- --:--:-- --:--:--   614
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   179  100    35  100   144    573   2359 --:--:-- --:--:-- --:--:--  2360
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   131  100    35  100    96    534   1465 --:--:-- --:--:-- --:--:--  1476
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   181  100    35  100   146    585   2443 --:--:-- --:--:-- --:--:--  2474
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   422  100   422    0     0   1352      0 --:--:-- --:--:-- --:--:--  1356
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    48  100    48    0     0    519      0 --:--:-- --:--:-- --:--:--   521
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   243  100    99  100   144   1032   1502 --:--:-- --:--:-- --:--:--  1515
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    12  100    12    0     0    220      0 --:--:-- --:--:-- --:--:--   222
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   422  100   422    0     0   9714      0 --:--:-- --:--:-- --:--:--  9813
sleeping 60 seconds and then collecting logs in case problems with jobs
resultlog/csa-managedb-pass.log
resultlog/csa-managedb-unauth.log
resultlog/csa-migrate-index-pass.log
resultlog/csa-migrate-index-unauth.log
resultlog/csa-migrate-view-pass.log
resultlog/csa-migrate-view-unauth.log
resultlog/csa-migrate-worker.log
[root@cl11c74lb1 test]# pwd
/root/software/cloudant-specialapi-27.0.2/test
[root@cl11c74lb1 test]# ls
csa-testall.sh             csa-test-managedb-unauth.sh     csa-test-migrate-index-unauth.sh  csa-test-migrate-view-unauth.sh  testindex
csa-test-managedb-pass.sh  csa-test-migrate-index-pass.sh  csa-test-migrate-view-pass.sh     resultlog                        testview
[root@cl11c74lb1 test]# ./csa-testall.sh
Username: northamd
Password:
Cluster URL (including http(s)): https://cl11c74vip.ibm.com
running managedb tests
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    72  100    72    0     0    885      0 --:--:-- --:--:-- --:--:--   888
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    82  100    82    0     0   1744      0 --:--:-- --:--:-- --:--:--  1782
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    64  100    64    0     0   1442      0 --:--:-- --:--:-- --:--:--  1454
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   518  100   518    0     0   6680      0 --:--:-- --:--:-- --:--:--  6727
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    21  100    21    0     0     94      0 --:--:-- --:--:-- --:--:--    95
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   458  100   458    0     0   6378      0 --:--:-- --:--:-- --:--:--  6450
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    12  100    12    0     0    144      0 --:--:-- --:--:-- --:--:--   144
running migrate-view tests
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    12  100    12    0     0    131      0 --:--:-- --:--:-- --:--:--   131
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    21  100    21    0     0    151      0 --:--:-- --:--:-- --:--:--   152
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   804  100   114  100   690    604   3657 --:--:-- --:--:-- --:--:--  3670
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   804  100   114  100   690   1380   8358 --:--:-- --:--:-- --:--:--  8414
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   816  100   114  100   702   1382   8510 --:--:-- --:--:-- --:--:--  8560
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    84  100    84    0     0    676      0 --:--:-- --:--:-- --:--:--   677
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   757  100    67  100   690   1669  17192 --:--:-- --:--:-- --:--:-- 17250
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   748  100    58  100   690   1378  16393 --:--:-- --:--:-- --:--:-- 16428
running migrate-index tests
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    12  100    12    0     0    167      0 --:--:-- --:--:-- --:--:--   169
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    21  100    21    0     0    169      0 --:--:-- --:--:-- --:--:--   169
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   255  100   111  100   144   1381   1792 --:--:-- --:--:-- --:--:--  1800
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   207  100   111  100    96   1270   1099 --:--:-- --:--:-- --:--:--  1275
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   257  100   111  100   146   1487   1956 --:--:-- --:--:-- --:--:--  1946
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   565  100   565    0     0   6526      0 --:--:-- --:--:-- --:--:--  6569
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    12  100    12    0     0    145      0 --:--:-- --:--:-- --:--:--   146
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   243  100    99  100   144   2274   3309 --:--:-- --:--:-- --:--:--  3348
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    12  100    12    0     0    246      0 --:--:-- --:--:-- --:--:--   250
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   422  100   422    0     0   8286      0 --:--:-- --:--:-- --:--:--  8440
sleeping 60 seconds and then collecting logs in case problems with jobs
resultlog/csa-managedb-pass.log
resultlog/csa-managedb-unauth.log
resultlog/csa-migrate-index-pass.log
resultlog/csa-migrate-index-unauth.log
resultlog/csa-migrate-view-pass.log
resultlog/csa-migrate-view-unauth.log
resultlog/csa-migrate-worker.log
```
  
The results are placed in a tarball and can be inspected.
  
```
[root@cl11c74lb1 resultlog]# ls -ltr
total 56
-rw-rw-r-- 1 root root     0 Aug 29 17:44 dummy
-rw-r--r-- 1 root root  3041 Aug 29 17:57 resultlog-%Y0829175431.tar
-rw-r--r-- 1 root root  1488 Sep 13 13:29 resultlog-%Y0913132619.tar
-rw-r--r-- 1 root root  1497 Sep 13 13:47 resultlog-20180913134407.tar
-rw-r--r-- 1 root root  1737 Sep 13 14:01 resultlog-20180913135739.tar
-rw-r--r-- 1 root root   312 Sep 13 14:04 csa-managedb-unauth.log
-rw-r--r-- 1 root root  1148 Sep 13 14:04 csa-managedb-pass.log
-rw-r--r-- 1 root root   766 Sep 13 14:06 csa-migrate-view-pass.log
-rw-r--r-- 1 root root   208 Sep 13 14:06 csa-migrate-view-unauth.log
-rw-r--r-- 1 root root  1261 Sep 13 14:06 csa-migrate-index-pass.log
-rw-r--r-- 1 root root   731 Sep 13 14:06 csa-migrate-index-unauth.log
-rw-r--r-- 1 root root 10487 Sep 13 14:07 csa-migrate-worker.log
-rw-r--r-- 1 root root  2899 Sep 13 14:07 resultlog-20180913140430.tar
[root@cl11c74lb1 resultlog]# tar xvf resultlog-20180913140430.tar
resultlog/csa-managedb-pass.log
resultlog/csa-managedb-unauth.log
resultlog/csa-migrate-index-pass.log
resultlog/csa-migrate-index-unauth.log
resultlog/csa-migrate-view-pass.log
resultlog/csa-migrate-view-unauth.log
resultlog/csa-migrate-worker.log
```
Here is an example set of the 'expected fail' results logs

```
[root@cl11c74lb1 resultlog]# cat resultlog/*unauth.log
READ db - fail unauthorised
{"error":"forbidden","reason":"You are not allowed to access this db."}

CREATE db - fail unauthorised
{"error":"forbidden","reason":"server_admin access is required for this request"}

DELETE db - fail unauthorised
{"error":"unauthorized","reason":"You are not a server admin."}

CREATE two index direct - expect fail

{"error":"error_saving_ddoc","reason":"Unknown error while saving the design document: forbidden"}

DELETE existing index direct - expect fail - cluster always returns ok so use list to check

{"ok":true}

LIST all index in testindexdb direct check index3 still exists

{"total_rows":3,"indexes":  
[{"ddoc":null,"name":"_all_docs",  
"type":"special","def":{"fields":[{"_id":"asc"}]}},  
{"ddoc":"_design/a2f1638c3858083beb17305e7601aeda925ee035",  "name":"potilaanSyntymaAika-index2",  
"type":"json","def":{"fields":[{"potilaanSyntymaAika.value":"asc"}]}},{"ddoc":"_design/potilaanSyntymaAika3",  
"name":"potilaanSyntymaAika-index3","type":"json",  
"def":{"fields":[{"potilaanSyntymaAika.value":"asc"}]}}]}
CREATE new view direct - expect fail

{"error":"forbidden","reason":"You are not a db or server admin."}

UPDATE existing view direct - expect fail

{"error":"conflict","reason":"Document update conflict."}  

```

Here is an example set of the 'expected pass' results logs

```
cat resultlog/*pass.log
cat: cat: No such file or directory

READ db via api - pass

{"update_seq": "9030-g1AAAAG7eJzLYWBg4MhgTmGQTs7JL01JzCtxSM4xNEw2N0lJMtTLTMrVS87PzQEqYkpkSJL__  
_9_VhIDA0shUTqSFIBkkj1MUz9xmhxAmuJJtCkBpKkepqmMKE15LECSo  
QFIAfXNB2sMIkHjAojG_WCNKiRoPADReB-ssZ0EjQ8gGiF-TMoCAFXAhvw",  
 "disk_size": 69445344, "sizes": {"active": 17636513, "external": 16607053, "file": 69445344},   
 "purge_seq": 0, "doc_count": 8894, "compact_running": false, "db_name": "metrics", "data_size": 17636513,  
  "doc_del_count": 0, "instance_start_time": "0", "other":   
  {"data_size": 16607053}, "disk_format_version": 6}
CREATE db via api - expect pass

{
  "result": "ok"
}

READ newly created db via api - expect pass

{"update_seq": "8-g1AAAAGjeJzLYWBg4MhgTmGQTs7JL01JzCtxSM4xNEw2N0lJMtTL  TMrVS87PzQEqYkpkSJL___9_  
ViIjUcqTFIBkkj0pOhxAOuJJ0ZEA0lFPgo48FiDJ0ACkg  
Jrmk6ZrAUTXftJ0HYDouk-argcQXSB_ZQEAuS-Dlg",  
 "disk_size": 66792, "sizes": {"active": 0, "external": 0, "file": 66792},  
  "purge_seq": 0, "doc_count": 0, "compact_running": false, "db_name": "newdb1000000",   
  "data_size": 0, "doc_del_count": 0, "instance_start_time": "0", "other":   
  {"data_size": 0}, "disk_format_version": 6}
DELETE db via api - expect pass
{"ok": true}

DELETE any testindexdb via api - expect pass

{"ok": true}
CREATE testindexdb via api - expect pass

{
  "result": "ok"
}

SUBMIT CREATE three index via api - pass

{"rev": "1-7bd1a09a2b43bb0bc2dcc2fa277424c6", "ok": true,   
"id": "testindexdb100000_index_20180913140631920969"}  
{"rev": "1-da5ee78b436cb52d67d3373549643d51", "ok": true,  
 "id": "testindexdb100000_index_20180913140632006934"}  
 {"rev": "1-668822ff24b4d075cee4db2c7e92edbd", "ok": true,  
  "id": "testindexdb100000_index_20180913140632092244"}
sleeping 20 seconds to allow jobs to be serviced before list attempt

LIST all index in testindexdb direct ie not via api - pass

{"total_rows":4,"indexes":  
[{"ddoc":null,"name":"_all_docs","type":"special","def":  
{"fields":[{"_id":"asc"}]}},{"ddoc":"_design/a2f1638c3858083beb17305e7601aeda925ee035",  
"name":"potilaanSyntymaAika-index2","type":"json","def":  
{"fields":[{"potilaanSyntymaAika.value":"asc"}]}},  
{"ddoc":"_design/potilaanSyntymaAika",  
"name":"potilaanSyntymaAika-index","type":"json","def":  
{"fields":[{"potilaanSyntymaAika.value":"asc"}]}},  
{"ddoc":"_design/potilaanSyntymaAika3",  
"name":"potilaanSyntymaAika-index3","type":"json","def":  
{"fields":[{"potilaanSyntymaAika.value":"asc"}]}}]}

SUBMIT DELETE existing index  via api - expect pass

{"ok": true}
DELETE any testviewdb via api - expect pass

{"ok": true}
CREATE testviewdb via api - expect pass

{
  "result": "ok"
}

SUBMIT CREATE two new views via api - pass

{"rev": "1-5150bc8ff5d52ad182126d9a6025940c", "ok": true,   
"id": "testviewdb100000_pmkctest1_20180913140431180495"}
{"rev": "1-1698b071ad4e14aff00a9cd621db3561", "ok": true,  
 "id": "testviewdb100000_pmkctest2_20180913140431320453"}
SUBMIT UPDATE existing view vai api - pass

{"rev": "1-61a370ec6eae8c013b1fba0863b696cb", "ok": true,  
 "id": "testviewdb100000_pmkctest2_20180913140431408163"}
sleeping 120 seconds to allow jobs to be serviced before deletion attempt

SUBMIT DELETE existing view  via api - expect pass

{"rev": "3-1280fc2077c6e3a649e62b1a5eb5ea70", "ok": true,  
 "id": "_design/pmkctest2"}
```
The migrate_worker.log is also partly captured to inspect the job activity during the tests
  
```
[root@cl11c74lb1 resultlog]# cat resultlog/csa-migrate-worker.log

2018-09-13 13:59:26,780[<module>] (MainProcess) {'error': 'API Access Session Error (503)'}/503
2018-09-13 13:59:36,795[<module>] (MainProcess) {'error': 'API Access Session Error (503)'}/503
2018-09-13 14:04:38,277[acquire_ownership_item] (MainProcess) {View Migrater} Acquire Ownership Success for Entry [testviewdb100000_pmkctest1_20180913140431180495]
2018-09-13 14:04:38,283[<module>] (MainProcess) {View Migrater} Executing DesignDoc Creation for Entry [testviewdb100000_pmkctest1_20180913140431180495]
2018-09-13 14:04:38,283[putddoc] (MainProcess) {View Migrater} Create : Starting
2018-09-13 14:04:40,312[wait_view_complete] (MainProcess) {View Migrater} Create FinishedCheck : Starting
2018-09-13 14:04:40,330[wait_view_complete] (MainProcess) {View Migrater} Create FinishedCheck : Progress [Detected Complete]
2018-09-13 14:04:50,332[execute_create] (MainProcess) {View Migrater} Complete for Entry [testviewdb100000_pmkctest1_20180913140431180495]
2018-09-13 14:04:50,381[acquire_ownership_item] (MainProcess) {View Migrater} Acquire Ownership Success for Entry [testviewdb100000_pmkctest2_20180913140431320453]
2018-09-13 14:04:50,388[<module>] (MainProcess) {View Migrater} Executing DesignDoc Creation for Entry [testviewdb100000_pmkctest2_20180913140431320453]
2018-09-13 14:04:50,388[putddoc] (MainProcess) {View Migrater} Create : Starting
2018-09-13 14:04:52,416[wait_view_complete] (MainProcess) {View Migrater} Create FinishedCheck : Starting
2018-09-13 14:04:52,428[wait_view_complete] (MainProcess) {View Migrater} Create FinishedCheck : Progress [Detected Complete]
2018-09-13 14:05:02,438[execute_create] (MainProcess) {View Migrater} Complete for Entry [testviewdb100000_pmkctest2_20180913140431320453]
2018-09-13 14:05:02,506[acquire_ownership_item] (MainProcess) {View Migrater} Acquire Ownership Success for Entry [testviewdb100000_pmkctest2_20180913140431408163]
2018-09-13 14:05:02,516[<module>] (MainProcess) {View Migrater} Executing Move and Switch DesignDoc Migration for Entry [testviewdb100000_pmkctest2_20180913140431408163]
2018-09-13 14:05:02,516[copyold] (MainProcess) {View Migrater} CopyOld Step : Starting
2018-09-13 14:05:04,556[putddoc] (MainProcess) {View Migrater} PutNew : Starting
2018-09-13 14:05:36,605[wait_view_complete] (MainProcess) {View Migrater} PutNew FinishedCheck : Starting
2018-09-13 14:05:36,640[wait_view_complete] (MainProcess) {View Migrater} PutNew FinishedCheck : Progress [Detected Complete]
2018-09-13 14:05:56,671[copyfinal] (MainProcess) {View Migrater} CopyFinal Step : Starting
2018-09-13 14:06:01,722[delnew] (MainProcess) {View Migrater} DeleteTemps Step (New): Starting
2018-09-13 14:06:03,785[delold] (MainProcess) {View Migrater} DeleteTemps Step (Old): Starting
2018-09-13 14:06:03,822[execute_moveandswitch] (MainProcess) {View Migrater} Complete for Entry [testviewdb100000_pmkctest2_20180913140431408163]
2018-09-13 14:06:34,024[acquire_ownership_item] (MainProcess) {View Migrater} Acquire Ownership Success for Entry [testindexdb100000_index_20180913140631920969]
2018-09-13 14:06:34,024[<module>] (MainProcess) {Index Migrater} Executing Index Creation for Entry [testindexdb100000_index_20180913140631920969]
2018-09-13 14:06:34,024[postindex] (MainProcess) {Index Migrater} Create : Starting
2018-09-13 14:06:34,078[postindex] (MainProcess) {Index Migrater} : Completed Successully
2018-09-13 14:06:34,125[acquire_ownership_item] (MainProcess) {View Migrater} Acquire Ownership Success for Entry [testindexdb100000_index_20180913140632006934]
2018-09-13 14:06:34,125[<module>] (MainProcess) {Index Migrater} Executing Index Creation for Entry [testindexdb100000_index_20180913140632006934]
2018-09-13 14:06:34,125[postindex] (MainProcess) {Index Migrater} Create : Starting
2018-09-13 14:06:34,178[postindex] (MainProcess) {Index Migrater} : Completed Successully
2018-09-13 14:06:34,218[acquire_ownership_item] (MainProcess) {View Migrater} Acquire Ownership Success for Entry [testindexdb100000_index_20180913140632092244]
2018-09-13 14:06:34,218[<module>] (MainProcess) {Index Migrater} Executing Index Creation for Entry [testindexdb100000_index_20180913140632092244]
2018-09-13 14:06:34,219[postindex] (MainProcess) {Index Migrater} Create : Starting
2018-09-13 14:06:34,249[postindex] (MainProcess) {Index Migrater} : Completed Successully
```







