import json
import datetime
import sys
import os
import base64
import logging
import time
import requests
from api_utils import * 
from perfagent_menu import *

def log_entry(location,filename,istring):
      if os.path.exists(location):
        lf = open(location+'/'+filename,'a')
        lf.write(str(istring)+'\n')
        lf.flush()
        lf.close()


def generate_repldoc(src_url,src_cred,src_cookie,dest_url,dest_cred,dest_cookie,src_username,proxy_url,certverif,authmethod,srcdb,destdb):
    doc = {}
    createtarget = True
    continuous = False
    start = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    id = ("metrics_shrinkrepl_started_"+start);
    if authmethod == 'cookie':
      src_cookie_header = {"Cookie": src_cookie}
      dest_cookie_header = {"Cookie": dest_cookie}
      target = {"url":dest_url+'/'+destdb,"headers":dest_cookie_header}
      source = {"url":src_url+'/'+srcdb,"headers":src_cookie_header}
    else:
      src_basic_header = {"Authorization": "Basic " + src_cred}
      dest_basic_header = {"Authorization": "Basic " + dest_cred}
      target = {"url":dest_url+'/'+destdb,"headers":dest_basic_header}
      source = {"url":src_url+'/'+srcdb,"headers":src_basic_header}
    user_roles = []
    user_roles.append('_admin')
    user_ctx = {"name":src_username,"roles": user_roles}
    if proxy_url:
       doc = {"_id":id,"source":source,"create_target":createtarget,"continuous":continuous,"target":target,"user_ctx":user_ctx,"proxy":proxy_url}
    else:
       doc = {"_id":id,"source":source,"create_target":createtarget,"continuous":continuous,"target":target,"user_ctx":user_ctx}
    return doc




def set_permissions_db(c_session,url,db,securitydoc):
     try:
      db_url = url+'/'+db + '/_security'
      json_doc = json.loads(securitydoc)
      thisrev = get_doc_rev(c_session,url+'/'+db,'_security')
      if len(thisrev) > 0:
        json_doc['_rev'] = thisrev
      doc_response = c_session.put(db_url,data=json.dumps(json_doc),headers={'content-type':'application/json'})
      if doc_response is None:
        logging.warn("Set Permissions DB Session put error: No response")
        return False
      if doc_response.status_code > 250:
        logging.warn("Set Permissions DB Session put error: " + str(doc_response.status_code))
        return False
      else:
        data = doc_response.json()
        if 'error' in data:
           logging.warn("Set Permissions DB Session put error: " + str(data))
           return False
        else:
          return True
     except Exception,e:
       logging.warn("Error Exception is ["+str(e)+"]")
       return False


def get_template(filename):
    doc = None
    if os.path.exists(filename):
      f = open(filename,'r')
      doc =  f.read()
      f.close()
    return doc


def make_db(c_session,url,db,permissions):
    dbmake_response = c_session.put(url+'/'+db,
        headers={'content-type': 'application/json'})
    if dbmake_response is None:
        print("Error making db [" + db +"] : No response from cluster")
        logging.warn("Error making db [" + db +"] : No response from cluster")
        return False
    elif dbmake_response.status_code < 250 or dbmake_response.status_code == 404:
        securitydoc = get_template(permissions)
        set_permissions_db(c_session,url,db,securitydoc)        
        return True
    elif dbmake_response.status_code >= 500 or dbmake_response.status_code == 400:
        print("Error making  db [" + db +"] : " + str(dbmake_response.status_code)+ "["+str(dbmake_response.content).rstrip()+"]")
        logging.warn("Error making  db [" + db +"] : " + str(dbmake_response.status_code)+ "["+str(dbmake_response.content).rstrip()+"]")
        return False
    elif dbmake_response.status_code >= 250:
        print("Error making  db [" + db +"] : " + str(dbmake_response.status_code))
        logging.warn("Error making db [" + db + "] : " + str(dbmake_response.status_code))
        return False

def drop_db(c_session,url,db):
    dbdelete_response = c_session.delete(url+'/'+db,
        headers={'content-type': 'application/json'})
    if dbdelete_response is None:
        print("Error deleting db [" + db +"] : No response from cluster")
        logging.warn("Error deleting db [" + db +"] : No response from cluster")
        return False
    elif dbdelete_response.status_code < 250 or dbdelete_response.status_code == 404:
        return True
    elif dbdelete_response.status_code >= 500 or dbdelete_response.status_code == 400:
        print("Error deleting  db [" + db +"] : " + str(dbdelete_response.status_code)+ "["+str(dbdelete_response.content).rstrip()+"]")
        logging.warn("Error deleting  db [" + db +"] : " + str(dbdelete_response.status_code)+ "["+str(dbdelete_response.content).rstrip()+"]")
        return False
    elif dbdelete_response.status_code >= 250:
        print("Error deleting  db [" + db +"] : " + str(dbdelete_response.status_code))
        logging.warn("Error deleting db [" + db + "] : " + str(dbdelete_response.status_code))
        return False




def reload_view(c_session,endpoint,docname):
    test_response = get_with_retries(c_session,endpoint,2,None)
    if test_response is None:
       logging.warn("Reload View get error: No response")
    elif test_response.status_code < 250:
        ddoc = get_ddoc(docname)
        if not ddoc:
            logging.warn("Reload View : Error updating designdoc for endpoint [" + endpoint +"] : Design doc [" + docname + "] not found")
            return False
        else:
          currentrev = get_doc_rev(c_session,endpoint,'')
          if currentrev:
           json_ddoc = json.loads(ddoc)
           json_ddoc['_rev'] = currentrev
           ddoc_response = c_session.put(endpoint,data=json.dumps(json_ddoc),headers={'content-type':'application/json'})
           if ddoc_response.status_code > 250:
            print("Reload View : Error updating designdoc for endpoint [" + endpoint +"] : " + str(ddoc_response.status_code))
            logging.warn("Reload View : Error updating designdoc for endpoint [" + endpoint +"] : " + str(ddoc_response.status_code))
            return False
           else:
            return True
          else:
            logging.warn("Reload View : Error updating designdoc for endpoint [" + endpoint +"] : Could not determine current revision")
            return False

    elif test_response.status_code == 404:
        ddoc = get_ddoc(docname)
        if not ddoc:
            logging.warn("Reload View : Error creating designdoc for endpoint [" + endpoint +"] : Design doc [" + docname + "] not found")
            return False
        else:
          ddoc_response = c_session.put(endpoint,data=ddoc,headers={'content-type':'application/json'})
          if ddoc_response.status_code > 250:
            logging.warn("Error creating designdoc for endpoint [" + endpoint +"] : " + str(ddoc_response.status_code))
            return False
          else:
            return True
    else:
      logging.warn("Reload View session error for endpoint [" + endpoint +"] : " + str(test_response.status_code))
      return False

def copy_doc(sess,src,dest,docid):
    doc_response = get_with_retries(sess,src+'/'+docid,2,None)
    if doc_response and doc_response.status_code < 250:
      docdata=doc_response.json()
      if '_rev' in docdata:
        del(docdata['_rev'])
      put_response = sess.put(dest+'/'+docid,data=json.dumps(docdata),headers={'content-type':'application/json'})
      if put_response is None or put_response.status_code > 250:
        if put_response.status_code > 250:
         logging.warn("Error copying doc [" + str(docid) +"] : " + str(put_response.status_code))

def execute_metrics_shrinker(sess,clusterurl,startkey,repldoc):
 try:
  if reload_view(sess,clusterurl+'/metrics/_design/daily_view','stats_by_day'):
   if drop_db(sess,clusterurl,'metrics_tmp'):
    if make_db(sess,clusterurl,'metrics_tmp','/opt/cloudant-specialapi/metrics-permissions.info'):
     views_response = get_with_retries(sess,clusterurl+'/metrics/_all_docs?startkey="_design"&endkey="_design0"',2,None)
     if views_response is None or views_response.status_code > 250:
          if views_response.status_code > 250:
            logging.warn("Error copying views : " + str(views_response.status_code))
     else:
       vdata = views_response.json()
       if 'rows' in vdata:
        for doc in vdata['rows']:
          copy_doc(sess,clusterurl+'/metrics',clusterurl+'/metrics_tmp',doc['id']) 
        docs_response = get_with_retries(sess,clusterurl+'/metrics/_design/daily_view/_view/stats_by_day?startkey='+startkey,2,None)
        if docs_response is None or docs_response.status_code > 250:
         if docs_response.status_code > 250:
          logging.warn('{Metrics database shrinker} Error : '+str(docs_response.status_code))
        else:
          data = docs_response.json()
          if 'rows' in data:
           for doc in data['rows']:
            copy_doc(sess,clusterurl+'/metrics',clusterurl+'/metrics_tmp',doc['id']) 
           if drop_db(sess,clusterurl,'metrics'):
            if make_db(sess,clusterurl,'metrics','/opt/cloudant-specialapi/metrics-permissions.info'):
             sess.post(clusterurl+'/_replicator',data=json.dumps(repldoc),headers={'content-type':'application/json'})
             return True
    return False
 except Exception as e:
  logging.warn('{Metrics database shrinker} Error : '+str(e))
  return False
 
defaults_file = "/opt/cloudant-specialapi/perfagent.conf"
logfilename = '/var/log/metricshrinker.log'
logging.basicConfig(filename = logfilename, level=logging.WARN,
                    format='%(asctime)s[%(funcName)-5s] (%(processName)-10s) %(message)s',
                    )

try:    
  requests.urllib3.disable_warnings()
except:
  try:
    requests.packages.urllib3.disable_warnings()
  except:
    logging.warn("{Metrics database shrinker} Unable to disable urllib3 warnings")
    pass


if __name__ == '__main__':
 try:

    opts, args = options()
    valid_selection = False

    default_connectioninfo, default_certificate_verification,default_requests_ca_bundle,default_inputlogfile,default_thresholdsfile,\
     default_eventsexclusionsfile,default_statsexclusionsfile,default_scope,default_granularity,\
     default_performercount, default_resultslocation, default_outputformat = process_defaults_config(defaults_file)

    if not opts.resultslocation:
       opts.resultslocation = default_resultslocation

    if default_certificate_verification == 'True':
       opts.certverif = True
       if os.path.exists(default_requests_ca_bundle):
          os.environ['REQUESTS_CA_BUNDLE'] = default_requests_ca_bundle
       else:
          print("REQUESTS_CA_BUNDLE file ["+str(default_requests_ca_bundle)+"] does not exist - all sessions will fail")
          logging.warn("REQUESTS_CA_BUNDLE file ["+str(default_requests_ca_bundle)+"] does not exist - all sessions will fail")
    else:
       opts.certverif = False

    if not opts.connectioninfo:
       opts.connectioninfo = default_connectioninfo

    s_url,s_credentials,s_username,s_password,p_url = process_connection_info(opts.connectioninfo)

    if s_url is None or s_credentials is None or s_username is None or s_password is None:
          print("perfagent: Cannot process connection info [" + str(opts.connectioninfo) + "]")
          logging.warn("{Metrics database shrinker} Cannot process connection info [" + str(opts.connectioninfo) + "]")
          sys.exit(1)
    else:
      logging.warn("{Metrics database shrinker} Startup") 
      sess,sresp,scookie = create_cluster_session(s_url,s_username, s_password,p_url,opts.certverif)
      if sess == None:
        logging.warn("Metrics database shrinker} Cluster Access Error : Session Rejected")
      elif sresp is None:
        logging.warn("Metrics database shrinker} Cluster Access Error : Session No response")
      elif sresp.status_code > 250:
        logging.warn("Metrics database shrinker} Cluster Access Error : Session Error ["+str(sresp.status_code)+"]")
      else:
              repldoc = generate_repldoc(s_url,s_credentials,scookie,s_url,s_credentials,scookie,s_username,p_url,False,'basic','metrics_tmp','metrics')
              startkey = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("[%Y,%-m,%-d]")
              response = execute_metrics_shrinker(sess,s_url,startkey,repldoc)
              if response: 
                    print('{Metrics database shrinker} Metrics database shrink Completed Successfully for key ['+startkey+']') 
                    logging.warn('{Metrics database shrinker} Metrics database shrink Completed Successfully for key ['+startkey+']') 
              else:
                print('{Metrics database shrinker} Metrics database shrink Failed for key ['+startkey+']') 
                logging.warn('{Metrics database shrinker} Metrics database shrink Failed for key ['+startkey+']') 
      close_cluster_session(sess,s_url)
 except Exception as e:
  logging.warn("Metrics database shrinker : Unexpected Shutdown : Reason ["+str(e)+"]")
