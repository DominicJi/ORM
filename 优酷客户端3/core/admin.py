import os
from tcpclient import client_run
from lib import common
from conf import settings
admin_data={'session':None}

def register(client):
    while True:
        name=input('please input your name>>:').strip()
        if name=='q':break
        password=input('please input your password>>:').strip()
        pwd=input('please confirm your password>>:').strip()
        if password==pwd:
            send_dic={'type':'register','user_type':'admin','name':name,'password':common.get_uuid(password)}
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
        send_dic={'type':'login','user_type':'admin','name':name,'password':common.get_uuid(password)}
        back_dic=common.send_back(send_dic,client)
        if back_dic['flag']:
            admin_data['session']=back_dic['session']
            print(back_dic['msg'])
            break
        else:print(back_dic['msg'])

@common.login_auth('admin')
def upload_movie(client):
    up_list=common.get_all_file_by_path(settings.BASE_MOVIE_UP)
    if up_list:
        while True:
            for i,j in enumerate(up_list):
                print('%s:%s'%(i,j))
            choice=input('please choose movie number to upload>>:').strip()
            if choice=='q':return
            if choice.isdigit():
                choice=int(choice)
                if choice not in range(len(up_list)):
                    print('not in range')
                    continue
                file_name=up_list[choice]
                file_path=os.path.join(settings.BASE_MOVIE_UP,up_list[choice])
                file_size=os.path.getsize(file_path)
                file_md5=common.get_big_file_md5(file_path)
                send_dic={'type':'check_movie','session':admin_data['session'],'file_md5':file_md5}
                back_dic=common.send_back(send_dic,client)
                if not back_dic['flag']:
                    is_free=input('please set movie free or not >>:').strip()
                    if is_free:
                        is_free=1
                    else:
                        is_free=0
                    send_dic={'type':'upload_movie','session':admin_data['session'],'file_name':file_name,'file_md5':file_md5,
                              'file_size':file_size,'is_free':is_free
                              }
                    back_dic=common.send_back(send_dic,client,file_path)
                    if back_dic['flag']:
                        print(back_dic['msg'])
                        break
                    else:
                        print(back_dic['msg'])
                else:print(back_dic['msg'])
            else:print('choose must be a number')
    else:print('暂无可上传的影片')


@common.login_auth('admin')
def delete_movie(client):
    send_dic={'type':'get_movie_list','session':admin_data['session'],'movie_type':'all'}
    back_dic=common.send_back(send_dic,client)
    if back_dic['flag']:
        while True:
            movie_list=back_dic['movie_list']
            for i,j in enumerate(movie_list):
                print('%s:%s--%s'%(i,j[0],j[1]))
            choice=input('please choice movie number to delete>>:').strip()
            if choice.isdigit():
                choice=int(choice)
                if choice not in range(len(movie_list)):
                    print('not in range')
                    continue
                send_dic={'type':'delete_movie','session':admin_data['session'],'movie_id':back_dic['movie_list'][choice][2]}
                back_dic=common.send_back(send_dic,client)
                if back_dic['flag']:
                    print(back_dic['msg'])
                    break
                else:
                    print(back_dic['msg'])
            else:print('must be a number')
    else:print(back_dic['msg'])


@common.login_auth('admin')
def release_notice(client):
    while True:
        name=input('please input notice name>>:').strip()
        if name=='q':break
        content=input('please input notice content>>:').strip()
        send_dic={'type':'release_notice','session':admin_data['session'],'name':name,'content':content}
        back_dic=common.send_back(send_dic,client)
        if back_dic['flag']:
            print(back_dic['msg'])
            break
        else:print(back_dic['msg'])
fun_dic = { '1': register, '2': login, '3': upload_movie,
            '4': delete_movie, '5': release_notice,}


def run():
    client = client_run.client_conn()
    while True:
        print('''
            1.注册
            2.登录
            3.上传视频
            4.删除视频
            5.发布公告
        ''')
        choose = input('please choose>>:').strip()
        if 'q' == choose: break
        if choose not in fun_dic: continue
        fun_dic[choose](client)
    client.close()
