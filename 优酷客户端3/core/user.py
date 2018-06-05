import os
from conf import settings
from lib import common
from tcpclient import client_run
import time
user_data={'session':None,'is_vip':None}

def register(client):
    while True:
        name=input('please input your name>>:').strip()
        if name=='q':break
        password=input('please input your password>>:').strip()
        pwd=input('please confirm your password>>:').strip()
        if password==pwd:
            send_dic={'type':'register','user_type':'user','name':name,'password':common.get_uuid(password)}
            back_dic=common.send_back(send_dic,client)
            if back_dic['flag']:
                print(back_dic['msg'])
                break
            else:print(back_dic['msg'])
        else:print('password confirm failure')
def login(client):
    while True:
        name=input('please input your name>>:').strip()
        if name=='q':break
        password=input('please input your password>>:').strip()
        send_dic={'type':'login','user_type':'user','name':name,'password':common.get_uuid(password)}
        back_dic=common.send_back(send_dic,client)
        if back_dic['flag']:
            user_data['session']=back_dic['session']
            user_data['is_vip']=back_dic['is_vip']
            print(back_dic['msg'])
            print(back_dic['notice'])
            break
        else:print(back_dic['msg'])
@common.login_auth('user')
def buy_member(client):
    if user_data['is_vip']:
        print('你已经是会员了')
        return
    while True:
        buy=input('please choice buy or not>>:').strip()
        if buy=='y':
            send_dic={'type':'buy_member','session':user_data['session']}
            back_dic=common.send_back(send_dic,client)
            if back_dic['flag']:
                user_data['is_vip']=1
                print(back_dic['msg'])
                break
            else:print(back_dic['msg'])
        elif buy=='n':
            print('you choice not buy')
        else:
            return

@common.login_auth('user')
def get_movie_list(client):
    send_dic={'type':'get_movie_list','session':user_data['session'],'movie_type':'all'}
    back_dic=common.send_back(send_dic,client)
    if back_dic['flag']:
        for i,j in enumerate(back_dic['movie_list']):
            print('%s:%s--%s'%(i,j[0],j[1]))
    else:print(back_dic['msg'])
@common.login_auth('user')
def down_free_movie(client):
    while True:
        send_dic={'type':'get_movie_list','session':user_data['session'],'movie_type':'free'}
        back_dic=common.send_back(send_dic,client)
        if back_dic['flag']:
            for i,j in enumerate(back_dic['movie_list']):
                print('%s:%s--%s'%(i,j[0],j[1]))
            choice=input('please choose movie number to download>>;').strip()
            if choice=='q':return
            if choice.isdigit():
                choice=int(choice)
                if choice in range(len(back_dic['movie_list'])):
                    send_dic={'type':'download_movie','session':user_data['session'],'movie_type':'free','movie_id':back_dic['movie_list'][choice][2]}
                    back_dic=common.send_back(send_dic,client)
                    if back_dic['flag']:
                        if back_dic['wait_time']>0:
                            print('please wait a second>>')
                            time.sleep(back_dic['wait_time'])
                        recv_size=0
                        path=os.path.join(settings.BASE_MOVIE_DOWN,back_dic['file_name'])
                        with open(path,'wb')as f:
                            while recv_size<back_dic['file_size']:
                                data=client.recv(1024)
                                recv_size+=len(data)
                                f.write(data)
                                percent=recv_size/back_dic['file_size']
                                common.progress(percent)
                            print()
                    else:print(back_dic['msg'])
                else:print('not in range')
            else:print('must be a number')
        else:
            print(back_dic['msg'])
            break



@common.login_auth('user')
def down_charge_movie(client):
    while True:
        send_dic={'type':'get_movie_list','session':user_data['session'],'movie_type':'charge'}
        back_dic=common.send_back(send_dic,client)
        if back_dic['flag']:
            for i,j in enumerate(back_dic['movie_list']):
                print('%s:%s--%s'%(i,j[0],j[1]))
            choice=input('please choose movie number to download>>;').strip()
            if choice=='q':return
            if choice.isdigit():
                choice=int(choice)
                if choice in range(len(back_dic['movie_list'])):
                    if user_data['is_vip']:
                        buy=input('please pay 5 to upload this movie>>:').strip()
                    else:
                        buy=input('please pay 10 to buy this movie>>:').strip()
                    if not buy=='y':
                        return
                    send_dic={'type':'download_movie','session':user_data['session'],'movie_type':'charge','movie_id':back_dic[choice][2]}
                    back_dic=common.send_back(send_dic,client)
                    if back_dic['flag']:
                        recv_size=0
                        path=os.path.join(settings.BASE_MOVIE_DOWN,back_dic['file_name'])
                        with open(path,'wb')as f:
                            while recv_size<back_dic['file_size']:
                                data=client.recv(1024)
                                recv_size+=len(data)
                                f.write(data)
                                percent=recv_size/back_dic['file_size']
                                common.progress(percent)
                            print()
                    else:print(back_dic['msg'])
                else:print('not in range')
            else:print('choice must bea number')
        else:
            print(back_dic['msg'])
            break
@common.login_auth('user')
def check_download_record(client):
    send_dic={'type':'check_download_record','session':user_data['session']}
    back_dic=common.send_back(send_dic,client)
    if back_dic['flag']:
        for notice in back_dic['download_list']:
            print(notice)
    else:
        print(back_dic['msg'])
@common.login_auth('user')
def check_notice(client):
    send_dic={'type':'check_notice','session':user_data['session']}
    back_dic=common.send_back(send_dic,client)
    if back_dic['flag']:
        for notice in back_dic['notice_list']:
            print(notice)
    else:
        print(back_dic['msg'])

fun_dic = {'1': register, '2': login, '3': buy_member,'4': get_movie_list,
           '5': down_free_movie,'6': down_charge_movie,
           '7': check_download_record,'8': check_notice}


def run():
    client = client_run.client_conn()
    while True:
        print('''
                1.注册
                2.登录
                3.冲会员
                4.查看视频
                5.下载免费视频
                6.下载收费视频
                7.查看观影记录
                8.查看公告
        ''')
        choose = input('please choose>>:').strip()
        if 'q' == choose: break
        if choose not in fun_dic: continue
        fun_dic[choose](client)
    client.close()