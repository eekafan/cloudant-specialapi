from flask import request, Response
import json
import datetime
import logging
import api_utils

def process_index_post(request,sess,dbid):
    try:
     idx = request.get_json(force=True) 
     logging.warn(str(idx))
     now = datetime.datetime.now()
     qtime = now.strftime("%Y%m%d%H%M%S%f")
     submitted = now.strftime("%Y-%m-%d %H:%M:%S.%f")
     id = dbid+'_index_'+qtime
     requester = api_utils.find_requestuser(request)
     qdoc = {"db":dbid,"index":idx,"qtime":qtime,"submitted":submitted,"status":"submitted","requester":requester}
     logging.warn(str(qdoc))
     put_response = sess.put(request.url_root+'apimigratequeue/'+id,data=json.dumps(qdoc),headers={'content-type':'application/json'})
     if put_response is None:
      return {'error': 'API Access Error'},400
     elif put_response.status_code == 404:
      return {'error': 'API Access Error - DB not found'},404
     elif put_response.status_code > 250:
      return {'error': 'API Access Session Error ('+str(put_response.status_code)+')'},put_response.status_code
     else:
      data = put_response.json()
      datastring = json.dumps(data)
      return datastring,None 
    except Exception as e:
      return {'error': 'API Processing Error'+str(e)},500 

def process_put(request,sess,dbid,ddid):
    try:
     ddoc = request.get_json(force=True) 
     now = datetime.datetime.now()
     qtime = now.strftime("%Y%m%d%H%M%S%f")
     submitted = now.strftime("%Y-%m-%d %H:%M:%S.%f")
     id = dbid+'_'+ddid+'_'+qtime
     requester = api_utils.find_requestuser(request)
     qdoc = {"db":dbid,"ddid":ddid,"ddoc":ddoc,"qtime":qtime,"submitted":submitted,"status":"submitted","requester":requester}
     put_response = sess.put(request.url_root+'apimigratequeue/'+id,data=json.dumps(qdoc),headers={'content-type':'application/json'})
     if put_response is None:
      return {'error': 'API Access Error'},400
     elif put_response.status_code == 404:
      return {'error': 'API Access Error - DB not found'},404
     elif put_response.status_code > 250:
      return {'error': 'API Access Session Error ('+str(put_response.status_code)+')'},put_response.status_code
     else:
      data = put_response.json()
      datastring = json.dumps(data)
      return datastring,None 
    except Exception as e:
      return {'error': 'API Processing Error'+str(e)},500 

def process_get(request,sess,docid):
     get_response = api_utils.get_with_retries(sess,request.url_root+'apimigratequeue/'+docid,5, None)
     if get_response is None:
      return {'error': 'API Access Error'},400
     elif get_response.status_code == 404:
      return {'error': 'API Access Error - DesignDocument Migrate Request Document not found'},404
     elif get_response.status_code > 250:
      return {'error': 'API Access Session Error ('+str(get_response.status_code)+')'},get_response.status_code
     else:
      data = get_response.json()
      datastring = json.dumps(data)
      return datastring,None

def process_index_delete(request,sess,dbid,ddid,iname):
     thisurl = request.url_root+dbid+'/_index/_design/'+ddid+'/json/'+iname
     del_response = sess.delete(thisurl)
     if del_response is None:
      return {'error': 'API Access Error'},400
     elif del_response.status_code > 250:
      return {'error': 'API Access Session Error ('+str(del_response.status_code)+')'},del_response.status_code
     else:
      data = del_response.json()
      datastring = json.dumps(data)
      return datastring,None

def process_delete(request,sess,dbid,ddid):
     thisurl = request.url_root+dbid+'/_design/'+ddid
     thisrev = api_utils.get_doc_rev(sess,request.url_root+dbid,'_design/'+ddid)
     print(thisurl+'?rev='+thisrev)
     del_response = sess.delete(thisurl+'?rev='+thisrev)
     if del_response is None:
      return {'error': 'API Access Error'},400
     elif del_response.status_code > 250:
      return {'error': 'API Access Session Error ('+str(del_response.status_code)+')'},del_response.status_code
     else:
      data = del_response.json()
      datastring = json.dumps(data)
      return datastring,None
