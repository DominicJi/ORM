import json
import struct
import hashlib
import time
from tcpserver import user_data

def send_back(back_dic,conn):
    head_json_bytes=json.dumps(back_dic).encode('utf-8')
    conn.send(struct.pack('i',len(head_json_bytes)))
    conn.send(head_json_bytes)

def get_session(name):
    md=hashlib.md5()
    md.update(name.encode('utf-8'))
    md.update(str(time.process_time()).encode('utf_8'))
    return md.hexdigest()

def login_auth(func):
    def wrapper(*args,**kwargs):
        for k in user_data.alive_user.values():
            if args[0]['session']==k[0]:
                args[0]['user_id']=k[1]
                break
        if not args[0].get('user_id',None):
            back_dic={'flag':False,'msg':'you are not in land'}
            send_back(back_dic,args[1])
        else:
            return func(*args,**kwargs)
    return wrapper
