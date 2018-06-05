import json
import struct
import hashlib
import os


def send_back(send_dic,client,file=None):
    head_json_bytes=json.dumps(send_dic).encode('utf-8')
    client.send(struct.pack('i',len(head_json_bytes)))
    client.send(head_json_bytes)
    if file:
        with open(file,'rb')as f:
            for line in f:
                client.send(line)
    back_info=client.recv(4)
    back_dic_len=struct.unpack('i',back_info)[0]
    back_dic=json.loads(client.recv(back_dic_len).decode('utf-8'))
    return back_dic

def get_uuid(password):
    md=hashlib.md5()
    md.update(password.encode('utf-8'))
    return md.hexdigest()

def get_all_file_by_path(path):
    return os.listdir(path)

def get_big_file_md5(path):
    if os.path.exists(path):
        md=hashlib.md5()
        file_size=os.path.getsize(path)
        count_list=[0,file_size//3,(file_size//3)*2,file_size-10]
        with open(path,'rb')as f:
            for i in count_list:
                f.seek(i)
                data=f.read(10)
                md.update(data)
        return md.hexdigest()

def login_auth(type):
    from core import admin,user
    def wrapper(func):
        def inner(*args,**kwargs):
            if type=='admin':
                if admin.admin_data['session']:
                    return func(*args,**kwargs)
                else:
                    print('please login first')
            elif type=='user':
                if user.user_data['session']:
                    return func(*args,**kwargs)
                else:
                    print('please login first')
        return inner
    return wrapper

def progress(percent,width=50):
    if percent>1:
        percent=1
    show_str=('[%%-%ds]'%width)%(int(percent*width)*'#')
    print('\r%s %s%%'%(show_str,int(percent*100)),end='')

