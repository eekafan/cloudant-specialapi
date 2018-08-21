from flask import request, Response
import json
import datetime
from api_utils import *

def process_get(request,sess,dbid):
     get_response = get_with_retries(sess,request.url_root+dbid,5, None)
     if get_response is None:
      return {'error': 'API Access Error'},400
     elif get_response.status_code == 404:
      return {'error': 'API Access Error - DB not found'},404
     elif get_response.status_code > 250:
      return {'error': 'API Access Session Error ('+str(get_response.status_code)+')'},get_response.status_code
     else:
      data = get_response.json()
      datastring = json.dumps(data)
      return datastring,None

def process_put(request,sess,dbid,qshards):
  try:
     put_response = None
     if qshards is not None:
      put_response = sess.put(request.url_root+dbid+'?q='+qshards,headers={'content-type':'application/json'})
     else:
      put_response = sess.put(request.url_root+dbid,headers={'content-type':'application/json'})
     if put_response is None:
      return {'error': 'API Access Error'},400
     elif put_response.status_code == 412:
      return {'error': 'API Access Error - Already Exists'},500
     elif put_response.status_code > 250:
      return {'error': 'API Access Session Error ('+str(put_response.status_code)+')'},put_response.status_code
     else:
      requestuser = find_requestuser(request)
      if requestuser is not None:
        securitydoc = str('{"admins":{"names":[],"roles":[]},"members":{"names":["' + str(requestuser) + '"],"roles":[]}}')
        if set_permissions_db(sess,request.url_root[:-1],dbid,securitydoc):
          return {'result':'ok'},200
      return {'error':'API Set Permissions Error'},500
  except Exception as e:
     return {'error':'API Unexpected Error ['+str(e)+']'},500

def process_delete(request,sess,dbid):
     delete_response = sess.delete(request.url_root+dbid,headers={'content-type':'application/json'})
     if delete_response is None:
      return {'error': 'API Access Error'},400
     elif delete_response.status_code == 404:
      return {'error': 'API Access Error - DB not found'},404
     elif delete_response.status_code > 250:
      return {'error': 'API Access Session Error ('+str(delete_response.status_code)+')'},delete_response.status_code
     else:
      data = delete_response.json()
      datastring = json.dumps(data)
      return datastring,None
