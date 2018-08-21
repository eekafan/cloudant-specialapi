from flask import Flask, abort, jsonify, make_response
from functools import wraps
from flask import request, Response
import json
import datetime
import sys
import base64
import logging
import api_utils 
import migrateapi
import managedbapi
import perfagentapi
import os
import requests

apiuser = ''
adminuser = ''
adminpwd = ''
clusterurl = ''
migrateapi_status = 'disabled'
managedbapi_status= 'disabled'
perfagentapi_status = 'disabled'

def check_auth(url,username, password):
    proxyurl = None
    certverif = False
    session,session_response,session_cookie = api_utils.create_cluster_session(url,username,password,proxyurl,certverif)
    if session is None:
     return False
    elif session_response is None:
     return False
    elif session_response.status_code > 250:
     return False
    else:
     api_utils.close_cluster_session(session,url)
     return True

def fail_authenticate():
    return make_response(jsonify({'error': 'Not Authenticated'}), 401)

def valid_user(username,cfile):
    if os.path.isfile(cfile):
     cf = open(cfile,'r')
     cflines = cf.readlines()
     match = False
     index = 0
     while not match and index < len(cflines):
      if cflines[index].strip() == username:
        match = True
      index = index + 1
     cf.close()
     return match
 
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        requestuser = api_utils.find_requestuser(request)
        if requestuser is None:
            return fail_authenticate()
        if not valid_user(requestuser,'/opt/cloudant-specialapi/csapi_users'):  
            return fail_authenticate()
        auth = request.authorization
        if auth and not check_auth(clusterurl,auth.username, auth.password):
            return fail_authenticate()
        return f(*args, **kwargs)
    return decorated
app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(503)
def not_supported(error):
    return make_response(jsonify({'error': 'Not Supported'}), 503)

@app.route('/_api')
def process_chk():
   return jsonify({'cloudant special api':'Welcome','version': '1.0.0'}) 
 
@app.route('/_api/migrate/<dbid>/_index',methods=['POST'])
@requires_auth
def migrate_index_post(dbid):
 try:
  if migrateapi_status == 'enabled':
   sess,err,code = api_utils.create_adminsession(clusterurl,adminuser, adminpwd)
   if err != None:
     return make_response(jsonify(err),code)
   else:
     if api_utils.create_db(sess,clusterurl,'apimigratequeue',adminuser):
      mresponse,mcode = migrateapi.process_index_post(request,sess,dbid)
      api_utils.close_cluster_session(sess,clusterurl)
      if mresponse and mcode is not None:
       return make_response(jsonify(mresponse),mcode)
      if mresponse and  mcode is None:
       return mresponse
  else:
   return make_response(jsonify({'error': 'API Disabled '}),503) 
 except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/migrate/<dbid>/_index/_design/<ddid>/json/<iname>',methods=['DELETE'])
@requires_auth
def migrate_index_delete(dbid,ddid,iname):
 try:
  if migrateapi_status == 'enabled':
   sess,err,code = api_utils.create_adminsession(clusterurl,adminuser, adminpwd)
   if err != None:
     return make_response(jsonify(err),code)
   else:
      mresponse,mcode = migrateapi.process_index_delete(request,sess,dbid,ddid,iname)
      api_utils.close_cluster_session(sess,clusterurl)
      if mresponse and mcode is not None:
       return make_response(jsonify(mresponse),mcode)
      if mresponse and  mcode is None:
       return mresponse
  else:
   return make_response(jsonify({'error': 'API Disabled '}),503) 
 except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/migrate/<dbid>/_design/<ddid>',methods=['PUT','POST'])
@requires_auth
def migrate_put(dbid,ddid):
 try:
  if migrateapi_status == 'enabled':
   sess,err,code = api_utils.create_adminsession(clusterurl,adminuser, adminpwd)
   if err != None:
     return make_response(jsonify(err),code)
   else:
     if api_utils.create_db(sess,clusterurl,'apimigratequeue',adminuser):
      mresponse,mcode = migrateapi.process_put(request,sess,dbid,ddid)
      api_utils.close_cluster_session(sess,clusterurl)
      if mresponse and mcode is not None:
       return make_response(jsonify(mresponse),mcode)
      if mresponse and  mcode is None:
       return mresponse
  else:
   return make_response(jsonify({'error': 'API Disabled '}),503) 
 except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/migrate/<dbid>/_design/<ddid>',methods=['DELETE'])
@requires_auth
def migrate_delete(dbid,ddid):
 try:
  if migrateapi_status == 'enabled':
   sess,err,code = api_utils.create_adminsession(clusterurl,adminuser, adminpwd)
   if err != None:
     return make_response(jsonify(err),code)
   else:
      mresponse,mcode = migrateapi.process_delete(request,sess,dbid,ddid)
      api_utils.close_cluster_session(sess,clusterurl)
      if mresponse and mcode is not None:
       return make_response(jsonify(mresponse),mcode)
      if mresponse and  mcode is None:
       return mresponse
  else:
   return make_response(jsonify({'error': 'API Disabled '}),503) 
 except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/migrate/<docid>',methods=['GET'])
@requires_auth
def migrate_get(docid):
 try:
  if migrateapi_status == 'enabled':
   sess,err,code = api_utils.create_adminsession(clusterurl,adminuser, adminpwd)
   if err != None:
     return make_response(jsonify(err),code)
   else:
      mresponse,mcode = migrateapi.process_get(request,sess,docid)
      api_utils.close_cluster_session(sess,clusterurl)
      if mresponse and mcode is not None:
       return make_response(jsonify(mresponse),mcode)
      if mresponse and  mcode is None:
       return mresponse
  else:
   return make_response(jsonify({'error': 'API Disabled '}),503) 
 except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/perfagent',methods=['POST'])
@requires_auth
def perfagent_post():
 try:
  if perfagentapi_status == 'enabled':
   sess,err,code = api_utils.create_adminsession(clusterurl,adminuser, adminpwd)
   if err != None:
     return make_response(jsonify(err),code)
   else:
     if api_utils.create_db(sess,clusterurl,'apiperfagentqueue',adminuser):
      mresponse,mcode = perfagentapi.process_post(request,sess)
      api_utils.close_cluster_session(sess,clusterurl)
      if mresponse and mcode is not None:
       return make_response(jsonify(mresponse),mcode)
      if mresponse and  mcode is None:
       return mresponse
  else:
   return make_response(jsonify({'error': 'API Disabled '}),503) 
 except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/perfagent/<docid>',methods=['GET'])
@requires_auth
def perfagent_get(docid):
 try:
  if perfagentapi_status == 'enabled':
   sess,err,code = api_utils.create_adminsession(clusterurl,adminuser, adminpwd)
   if err != None:
     return make_response(jsonify(err),code)
   else:
      mresponse,mcode = perfagentapi.process_get(request,sess,docid)
      api_utils.close_cluster_session(sess,clusterurl)
      if mresponse and mcode is not None:
       return make_response(jsonify(mresponse),mcode)
      if mresponse and  mcode is None:
       return mresponse
  else:
   return make_response(jsonify({'error': 'API Disabled '}),503) 
 except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 

@app.route('/_api/managedb/<dbid>',methods=['GET'])
@requires_auth
def managedb_get(dbid):
 try:
  if managedbapi_status == 'enabled':
   sess,err,code = api_utils.create_adminsession(clusterurl,adminuser, adminpwd)
   if err != None:
     return make_response(jsonify(err),code)
   else:
      mresponse,mcode = managedbapi.process_get(request,sess,dbid)
      api_utils.close_cluster_session(sess,clusterurl)
      if mresponse and mcode is not None:
       return make_response(jsonify(mresponse),int(mcode))
      if mresponse and  mcode is None:
       return mresponse
  else:
   return make_response(jsonify({'error': 'API Disabled '}),503) 
 except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 


@app.route('/_api/managedb/<dbid>',methods=['PUT'])
@requires_auth
def managedb_put(dbid):
 try:
  if managedbapi_status == 'enabled':
   sess,err,code = api_utils.create_adminsession(clusterurl,adminuser, adminpwd)
   if err != None:
     return make_response(jsonify(err),code)
   else:
      shardsq = request.args.get('q')
      mresponse,mcode = managedbapi.process_put(request,sess,dbid,shardsq)
      api_utils.close_cluster_session(sess,clusterurl)
      if mresponse and mcode is not None:
       return jsonify(mresponse),mcode
      if mresponse and  mcode is None:
       return mresponse
  else:
   return make_response(jsonify({'error': 'API Disabled '}),503) 
 except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 


@app.route('/_api/managedb/<dbid>',methods=['DELETE'])
@requires_auth
def managedb_delete(dbid):
 try:
  if managedbapi_status == 'enabled':
   sess,err,code = api_utils.create_adminsession(clusterurl,adminuser, adminpwd)
   if err != None:
     return make_response(jsonify(err),code)
   else:
      mresponse,mcode = managedbapi.process_delete(request,sess,dbid)
      api_utils.close_cluster_session(sess,clusterurl)
      if mresponse and mcode is not None:
       return make_response(jsonify(mresponse),mcode)
      if mresponse and  mcode is None:
       return mresponse
  else:
   return make_response(jsonify({'error': 'API Disabled '}),503) 
 except Exception as e:
      return make_response(jsonify({'error': 'API Processing Error ('+str(e)+')'}),500) 


logfilename = "/var/log/csapi.log"

logging.basicConfig(filename = logfilename, level=logging.WARN,
                    format='%(asctime)s[%(funcName)-5s] (%(processName)-10s) %(message)s',
                    )

try:    
  requests.urllib3.disable_warnings()
except:
  try:
    requests.packages.urllib3.disable_warnings()
  except:
    logging.warn("{csapi start} Unable to disable urllib3 warnings")
    pass

if __name__ == '__main__':
 try:
  clusterurl,creds,migrateapi_status,managedbapi_status,perfagentapi_status = api_utils.process_config('/opt/cloudant-specialapi/csapi.conf') 
  credparts = str(base64.urlsafe_b64decode(creds)).split(':')
  if len(credparts) == 2:
   adminuser = credparts[0]
   adminpwd = credparts[1]
   logging.warn("Startup : Cloudant Special API")
   app.run()
 except Exception as e:
  logging.warn("Exception Shutdown : Cloudant Special API: Error ["+str(e)+"]")
