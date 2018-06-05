import socket
import json
import struct
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from tcpserver import user_data
from lib import common
from conf import settings
from interface import admin_interface,user_interface,common_interface
pool=ThreadPoolExecutor(8)
mutex=Lock()
user_data.mutex=mutex
func_dic={'register':common_interface.register,'login':common_interface.login,'get_movie_list':common_interface.get_movie_list,
          'upload_movie':admin_interface.upload_movie,'delete_movie':admin_interface.delete_movie,'release_notice':admin_interface.release_notice,
          'buy_member':user_interface.buy_member,'download_movie':user_interface.download_movie,'check_download_record':user_interface.check_download_record,
          'check_notice':user_interface.check_notice,'check_movie':admin_interface.check_movie
          }
def working(conn,addr):
    while True:
        try:
            head_info=conn.recv(4)
            user_dic_len=struct.unpack('i',head_info)[0]
            user_dic=json.loads(conn.recv(user_dic_len).decode('utf-8'))
            user_dic['addr']=str(addr)
            dispatch(user_dic,conn)
        except Exception as a:
            print(a)
            conn.close()
            mutex.acquire()
            if str(addr) in user_data.alive_user:
                user_data.alive_user.pop(str(addr))
            mutex.release()
            print('client:%s break up link'%str(addr))
            break
def dispatch(user_dic,conn):
    if user_dic['type'] not in func_dic:
        back_dic={'flag':False,'msg':'请求不存在'}
        common.send_back(back_dic,conn)
    else:
        func_dic[user_dic['type']](user_dic,conn)
def run():
    server=socket.socket()
    server.bind(settings.server_address)
    server.listen(5)
    while True:
        conn,addr=server.accept()
        pool.submit(working,conn,addr)
    server.close()
