import json
import datetime
import sys
import os
import base64
import logging
import api_utils
import migrateapi
from worker_utils import process_queue,update_queue_entry
import time
import requests

def process_workerconfig(cfile):
    index_wait_timeout = 7200 
    if cfile and os.path.isfile(cfile):
      cf = open(cfile,'r')
      cflines = cf.readlines()
      for cfline in cflines:
          cflineparts = cfline.split()
          if len(cflineparts) == 2 and cflineparts[0] == 'index_wait_timeout':
            index_wait_timeout = int(cflineparts[1])
          else:
            pass
      cf.close()
    return index_wait_timeout 

def acquire_ownership_item(sess,clusterurl,qitem):
 try:
  itemurl = clusterurl+'/apimigratequeue/'+qitem['_id']
  status_response = api_utils.get_with_retries(sess,itemurl,2,None)
  if status_response is None:
        logging.warn("{View Migrater} Acquire Ownership Error for Entry ["+str(qitem['_id'])+"] : No response")
        return False
  elif status_response.status_code > 250:
        logging.warn("{View Migrater} Acquire Ownership Session for Entry ["+str(qitem['_id'])+"] Error : " + str(status_response.status_code))
        return False
  else:
     data = status_response.json()
     if 'status' in data:
      if data['status'] == 'submitted':
       if update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"processing",None,None): 
        logging.warn("{View Migrater} Acquire Ownership Success for Entry ["+str(qitem['_id'])+"] " )
        return True
       else:
        logging.warn("{View Migrater} Acquire Ownership Failed for Entry ["+str(qitem['_id'])+"] : could not update item" )
        return False
      else:
       logging.warn("{View Migrater} Acquire Ownership Failed for Entry ["+str(qitem['_id'])+"] : item owned by another worker" )
       return False
     else:
      logging.warn("{View Migrater} Acquire Ownership Failed for Entry ["+str(qitem['_id'])+"] : Failed to read item" )
      return False
 except Exception as e:
  logging.warn("{View Migrater} Acquire Ownership Unexpected Error for Entry ["+str(qitem['_id'])+"] : " + str(e))
  return False

def copyold(sess,clusterurl,qitem):
 try:
  fromurl = clusterurl+'/'+qitem['db']+'/_design/'+qitem['ddid']
  old = '_design/'+qitem['ddid']+'_OLD' 
  logging.warn("{View Migrater} CopyOld Step : Starting")
  copyold_response = sess.request('COPY',fromurl,headers={'Destination': old},verify=False)
  if copyold_response is None:
        logging.warn("{View Migrater} CopyOld Step Error: No response")
        update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","CopyOld Step Error : No response",None) 
        return False
  elif copyold_response.status_code > 250:
        logging.warn("{View Migrater} CopyOld Step Session Error : " + str(copyold_response.status_code))
        update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","CopyOld Step Session Error : " + str(copyold_response.status_code),None)
        return False
  else:
        return True
 except Exception as e:
  logging.warn("{View Migrater} CopyOld Step Error : " + str(e))
  return False

def postindex(sess,clusterurl,qitem,stepmarker):
 try:
  url =  clusterurl+'/'+qitem['db']+'/_index'
  logging.warn("{Index Migrater} "+str(stepmarker)+" : Starting")
  post_response = sess.post(url,data=json.dumps(qitem['index']),headers={'content-type':'application/json'})
  if post_response is None:
        logging.warn("{Index Migrater} "+str(stepmarker)+ " Error: No response")
        update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed",str(stepmarker)+ " Error : No Response",None) 
        return False
  elif post_response.status_code > 250:
        logging.warn("{Index Migrater} "+str(stepmarker)+" Session Error : " + str(put_response.status_code))
        update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed",str(stepmarker)+ " Session Error : " + str(put_response.status_code),None)
        return False
  else:
        data = post_response.json()
        if 'result' in data:
         if data['result'] == 'created':
          update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"completed",data,None) 
          logging.warn("{Index Migrater} : Completed Successully")
         else:
          update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed",data,None) 
          logging.warn("{Index Migrater} : Failed")
        else:
          update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","Empty result",None) 
          logging.warn("{Index Migrater} : Failed")
        return True
 except Exception as e:
  logging.warn("{Index Migrater} "+str(stepmarker) + " Error : " + str(e))
  return False

def putddoc(sess,clusterurl,qitem,ddid,stepmarker):
 try:
  url =  clusterurl+'/'+qitem['db']+'/_design/'+ddid
  logging.warn("{View Migrater} "+str(stepmarker)+" : Starting")
  put_response = sess.put(url,data=json.dumps(qitem['ddoc']),headers={'content-type':'application/json'})
  if put_response is None:
        logging.warn("{View Migrater} "+str(stepmarker)+ " Error: No response")
        update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed",str(stepmarker)+ " Error : No Response",None) 
        return False
  elif put_response.status_code > 250:
        logging.warn("{View Migrater} "+str(stepmarker)+" Session Error : " + str(put_response.status_code))
        update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed",str(stepmarker)+ " Session Error : " + str(put_response.status_code),None)
        return False
  else:
        return True
 except Exception as e:
  logging.warn("{View Migrater} "+str(stepmarker) + " Error : " + str(e))
  return False
  
def exists_currentview(sess,clusterurl,qitem):
 try:
  currenturl =  clusterurl+'/'+qitem['db']+'/_design/'+qitem['ddid']
  test_response = api_utils.get_with_retries(sess,currenturl,2,None)
  if test_response is None:
     logging.warn("{View Migrater} GetCurrentView: No response")
     return True
  elif test_response.status_code == 404:
     return False
  elif test_response.status_code > 250:
     logging.warn("{View Migrater} GetCurrentView Session get error: " + str(test_response.status_code))
     return True
  else:
     return True
 except Exception as e:
  logging.warn("{View Migrater} GetCurrent View Error : " + str(e))
  return True
  
def getview(sess,clusterurl,qitem,ddid):
 try:
  url =  clusterurl+'/'+qitem['db']+'/_design/'+ddid
  test_response = api_utils.get_with_retries(sess,url,2,None)
  if test_response is None:
     logging.warn("{View Migrater} GetView : No response")
     return None
  elif test_response.status_code == 404:
     logging.warn("{View Migrater} GetView : Not found")
     return None
  elif test_response.status_code > 250:
     logging.warn("{View Migrater} GetView Session get error: " + str(test_response.status_code))
     return None
  else:
     data = test_response.json()
     if 'views' in data:
       views = data['views'].keys()
       return str(views[0])
     else:
       return None
 except Exception as e:
  logging.warn("{View Migrater} GetView Unexpected Error : " + str(e))
  return None

def testview_buildcomplete(sess,clusterurl,qitem,ddid,view,timeout,stepmarker):
 try:
  viewurl =  clusterurl+'/'+qitem['db']+'/_design/'+ddid+'/_view/'+view+'?limit=1'
  headers = {'User-Agent':'csapimigrater','x-cloudant-io-priority':'low'}
  test_response = sess.request('GET',viewurl,timeout=timeout,headers=headers,verify=False)
  if test_response is None:
     logging.warn("{View Migrater} PutNew TestNewView: No response")
     return False
  elif test_response.status_code == 404:
     logging.warn("{View Migrater} PutNew TestNewView: Not found")
     return False
  elif test_response.status_code == 500:
     if "Read timed out" not in str(test_response.content):
      logging.warn("{View Migrater} PutNew TestNewView Session 500 Error: " + str(test_response.content))
     return False
  elif test_response.status_code > 250:
     if "Read timed out" not in str(test_response.content):
      logging.warn("{View Migrater} PutNew TestNewView Session get error: " + str(test_response.status_code))
     return False
  else:
     return True
 except Exception as e:
  if "Read timed out" not in str(e):
   logging.warn("{View Migrater} PutNew TestNewView Error : " + str(e))
  return False

def getindex_progress(sess,clusterurl,qitem,ddid,stepmarker):
 try:
    get_response = api_utils.get_with_retries(sess,clusterurl+'/_active_tasks',2,None)
    if get_response is None:
       logging.warn("{View Migrater} "+str(stepmarker)+" FinishedCheck GetProgress: No response")
       return None
    elif get_response.status_code == 404:
       logging.warn("{View Migrater} "+str(stepmarker)+" FinishedCheck GetProgress: Not found")
       return None
    elif get_response.status_code > 250:
       logging.warn("{View Migrater} "+str(stepmarker)+" FinishedCheck  GetProgress Session get error: " + str(get_response.status_code))
       return None
    else:
       data = get_response.json()
       progress = 0
       shards = 0 
       for task in data:
        if task['type'] == "indexer" and task['design_document'] == '_design/'+ddid:
          shards = shards +1
          progress = progress + int(task['progress'])
       if progress > 0 and shards > 0:
          overall_progress = progress/shards
          return overall_progress
       else:
        return None
 except Exception as e:
  logging.warn("{View Migrater} "+str(stepmarker) + "Finished Check GetProgess Error : " + str(e))
 return None 

def wait_view_complete(sess,clusterurl,qitem,ddid,view,index_wait_timeout,stepmarker):
 try:
       logging.warn("{View Migrater} "+str(stepmarker)+" FinishedCheck : Starting")
       index_wait = 0
       index_complete = False
       progress_detected = False
       test_timeout = float(10.0)
       progress_count = 25
       while (not index_complete) and  (index_wait < index_wait_timeout): 
        if testview_buildcomplete(sess,clusterurl,qitem,ddid,view,test_timeout,stepmarker):
         index_complete = True
         logging.warn("{View Migrater} "+str(stepmarker)+" FinishedCheck : Progress [Detected Complete]")
        else:
         index_wait = index_wait + int(test_timeout) + 10
         progress = getindex_progress(sess,clusterurl,qitem,ddid,stepmarker)
         if not progress_detected:
           if progress is not None:
              progress_detected = True
              logging.warn("{View Migrater} "+str(stepmarker) + " FinishedCheck : Progress [Indexing Detected]")
         else:
           if progress is not None:
              if progress < 75 and progress >= progress_count:
                 progress_count = progress_count + 25  
                 logging.warn("{View Migrater} " + str(stepmarker)+ " FinishedCheck : Progress ["+str(progress)+"%]")
              elif progress >= 75 and progress < 95 and progress >= progress_count:
                 progress_count = progress_count + 20  
                 logging.warn("{View Migrater} " + str(stepmarker)+ " FinishedCheck : Progress ["+str(progress)+"%]")
              elif progress >= 95 and progress >= progress_count:
                 progress_count = 100
                 logging.warn("{View Migrater} " + str(stepmarker)+ " FinishedCheck : Progress ["+str(progress)+"%]")
        time.sleep(10.0)
       if index_complete:
         return True
       else:
         return False 
 except Exception as e:
  logging.warn("{View Migrater} "+str(stepmarker) + " FinishedCheck Error : " + str(e))
  return False 

def copyfinal(sess,clusterurl,qitem): 
 try:
  # note issue 97653 : Destination should not include the db or a leading /
  newurl =  clusterurl+'/'+qitem['db']+'/_design/'+qitem['ddid']+'_NEW'
  finalrev = api_utils.get_doc_rev(sess,clusterurl+'/' + qitem['db'],'_design/'+qitem['ddid'])
  final = '_design/'+qitem['ddid']+'?rev='+finalrev
  logging.warn("{View Migrater} CopyFinal Step : Starting")
  copyfinal_response = sess.request('COPY',newurl,headers={'Destination': final},verify=False)
  if copyfinal_response is None:
        logging.warn("{View Migrater} CopyFinal Step Error: No response")
        update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","CopyFinal Step Error : No response",None) 
        return False
  elif copyfinal_response.status_code > 250:
        logging.warn("{View Migrater} CopyFinal Step Session Error : " + str(copyfinal_response.status_code))
        update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","CopyFinal Step Session Error : " + str(copyfinal_response.status_code),None)
        return False
  else:
        return True 
 except Exception as e:
  logging.warn("{View Migrater} CopyFinal Step Error : " + str(e))
  return False 

def delnew(sess,clusterurl,qitem):
 try:
  logging.warn("{View Migrater} DeleteTemps Step (New): Starting")
  newurl =  clusterurl+'/'+qitem['db']+'/_design/'+qitem['ddid']+'_NEW'
  new = '_design/'+qitem['ddid']+'_NEW' 
  newrev = api_utils.get_doc_rev(sess,clusterurl+'/'+qitem['db'],new)
  delnew_response = sess.delete(newurl+'?rev='+newrev)
  if delnew_response is None:
        logging.warn("{View Migrater} Deltemps Step (New) Error: No response")
        update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","Deltemps Step Error : No response",None) 
        return False
  elif delnew_response.status_code > 250:
        logging.warn("{View Migrater} Deltemps Step Session (New) Error : " + str(delnew_response.status_code))
        update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","Deltemps Step Session (New) Error : " + str(delnew_response.status_code),None)
        return False
  else:
        return True
 except Exception as e:
  logging.warn("{View Migrater} Deltemps Step (New) Error : " + str(e))
  return False 

def delold(sess,clusterurl,qitem):
 try:
  logging.warn("{View Migrater} DeleteTemps Step (Old): Starting")
  old = '_design/'+qitem['ddid']+'_OLD' 
  oldurl =  clusterurl+'/'+qitem['db']+'/_design/'+qitem['ddid']+'_OLD'
  oldrev = api_utils.get_doc_rev(sess,clusterurl+'/'+qitem['db'],old)
  delold_response = sess.delete(oldurl+'?rev='+oldrev)
  if delold_response is None:
        logging.warn("{View Migrater} Deltemps Step (Old) Error: No response")
        update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","Deltemps Step (Old) Error : No response",None) 
        return False
  elif delold_response.status_code > 250:
        logging.warn("{View Migrater} Deltemps Step (Old) Session Error : " + str(delold_response.status_code))
        update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","Deltemps Step (Old) Session Error : " + str(delold_response.status_code),None)
        return False
  else:
        return True
 except Exception as e:
  logging.warn("{View Migrater} Deltemps Step (Old) Error : " + str(e))
  return False 

def execute_index_create(sess,clusterurl,qitem):
 try:
   postindex(sess,clusterurl,qitem,'Create')
 except Exception as e:
  logging.warn("{Index Migrater} Execute Create Unexpected Error : " + str(e))
  update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","Create Unexpected Error : " + str(e),None)
  return False 

def execute_create(sess,clusterurl,qitem):
 try:
   if putddoc(sess,clusterurl,qitem,str(qitem['ddid']),'Create'):
     time.sleep(2.0)
     testview = getview(sess,clusterurl,qitem,str(qitem['ddid']))
     if testview is not None:
      if wait_view_complete(sess,clusterurl,qitem,str(qitem['ddid']),testview,index_wait_timeout,'Create'):
         logging.warn("{View Migrater} Complete for Entry ["+str(qitem['_id'])+"]")
         update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"success",None,None)
         return True
     else:
       update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","Create error : no view found inside doc",None)
       
   time.sleep(1.0)
   logging.warn("{View Migrater} Failures during Migration for Entry ["+str(qitem['_id'])+"]")
   return False
 except Exception as e:
  logging.warn("{View Migrater} Execute Create Unexpected Error : " + str(e))
  update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","Create Unexpected Error : " + str(e),None)
  return False 

def execute_moveandswitch(sess,clusterurl,index_wait_timeout,qitem):
 try:
  if copyold(sess,clusterurl,qitem):
   time.sleep(2.0)
   if putddoc(sess,clusterurl,qitem,str(qitem['ddid'])+'_NEW','PutNew'):
     time.sleep(2.0)
     testview = getview(sess,clusterurl,qitem,str(qitem['ddid'])+'_NEW')
     if testview is not None:
      time.sleep(30.0)
      if wait_view_complete(sess,clusterurl,qitem,str(qitem['ddid']+'_NEW'),testview,index_wait_timeout,'PutNew'):
       time.sleep(10.0)
       if copyfinal(sess,clusterurl,qitem): 
        time.sleep(5.0)
        if delnew(sess,clusterurl,qitem):
          time.sleep(2.0)
          if delold(sess,clusterurl,qitem):
             logging.warn("{View Migrater} Complete for Entry ["+str(qitem['_id'])+"]")
             update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"success",None,None)
             return True
  time.sleep(5.0)
  logging.warn("{View Migrater} Failures during Migration for Entry ["+str(qitem['_id'])+"]")
  logging.warn("{View Migrater} Cleanup : Starting") 
  delnew(sess,clusterurl,qitem)
  delold(sess,clusterurl,qitem)
  logging.warn("{View Migrater} Cleanup Complete for Entry ["+str(qitem['_id'])+"]")
  return False
 except Exception as e:
  logging.warn("{View Migrater} Execute Move and Switch Unexpected Error : " + str(e))
  return False 
 
adminuser = ''
adminpwd = ''

logfilename = '/var/log/migrateworker.log'
logging.basicConfig(filename = logfilename, level=logging.WARN,
                    format='%(asctime)s[%(funcName)-5s] (%(processName)-10s) %(message)s',
                    )

try:    
  requests.urllib3.disable_warnings()
except:
  try:
    requests.packages.urllib3.disable_warnings()
  except:
    logging.warn("{View Migrater} Unable to disable urllib3 warnings")
    pass


if __name__ == '__main__':
 try:
   logging.warn("{View Migrater} Startup") 
   clusterurl,creds,migrateapi_status,managedbapi_status,perfagentapi_status = api_utils.process_config('/opt/cloudant-specialapi/csapi.conf')
   credparts = str(base64.urlsafe_b64decode(str(creds))).split(':')
   if len(credparts) == 2:
    adminuser = credparts[0]
    adminpwd = credparts[1]
    index_wait_timeout = process_workerconfig('/opt/cloudant-specialapi/migrateworker.conf')
    while True:
     sess,serr,scode = api_utils.create_adminsession(clusterurl,adminuser, adminpwd)
     if serr != None:
      logging.warn(str(serr)+'/'+str(scode))
     else:
      qdata,qcode = process_queue(sess,clusterurl,'apimigratequeue') 
      if qdata is not None:
       if not 'error' in qdata: 
        for qitem in qdata:
         if acquire_ownership_item(sess,clusterurl,qitem):
          if 'ddoc' in qitem:
           if exists_currentview(sess,clusterurl,qitem):
            logging.warn('{View Migrater} Executing Move and Switch DesignDoc Migration for Entry ['+qitem['_id']+']') 
            execute_moveandswitch(sess,clusterurl,index_wait_timeout,qitem)
           else:
            logging.warn('{View Migrater} Executing DesignDoc Creation for Entry ['+qitem['_id']+']') 
            execute_create(sess,clusterurl,qitem) 
          elif 'index' in qitem:
            logging.warn('{Index Migrater} Executing Index Creation for Entry ['+qitem['_id']+']') 
            execute_index_create(sess,clusterurl,qitem)
          else:
            logging.warn('{View Migrater} Unrecognised Queue command for Entry ['+qitem['_id']+']') 
            update_queue_entry(sess,clusterurl,qitem,'apimigratequeue',"failed","Invalid Queue Item",None) 
       elif 'error' in qdata and qdata['error'] != "Queue Error = Empty": 
        logging.warn("{View Migrater} Error in processing queue ["+str(qdata)+"] Code ["+str(qcode)+"]")
     api_utils.close_cluster_session(sess,clusterurl)
     time.sleep(10)
 except Exception as e:
  logging.warn("Cloudant View Migrater : Unexpected Shutdown : Reason ["+str(e)+"]")
