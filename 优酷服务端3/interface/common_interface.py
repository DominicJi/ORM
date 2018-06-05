from db import models
from lib import common
from tcpserver import user_data
from interface import user_interface
@common.login_auth
def get_movie_list(user_dic,conn):
    movie_list=models.Movie.select_all()
    back_movie_list=[]
    if movie_list:
        for movie in movie_list:
            if not movie.is_delete:
                if user_dic['movie_type']=='all':
                    back_movie_list.append([movie.name,'免费' if movie.is_free else '收费',movie.id])
                elif user_dic['movie_type']=='free':
                    if movie.is_free:
                        back_movie_list.append([movie.name,'免费',movie.id])
                else:
                    if not movie.is_free:
                        back_movie_list.append([movie.name,'收费',movie.id])
        if back_movie_list:
            back_dic={'flag':True,'movie_list':back_movie_list}
        else:
            back_dic={'flag':False,'msg':'目前没有该类型的影片'}
    else:
        back_dic={'flag':False,'msg':'目前暂无任何影片'}
    common.send_back(back_dic,conn)

def register(user_dic,conn):
    user=models.User.select_one(name=user_dic['name'])
    if user:
        back_dic={'flag':False,'msg':'username has existed'}
    else:
        user=models.User(name=user_dic['name'],password=user_dic['password'],user_type=user_dic['user_type'])
        user.save()
        back_dic={'flag':True,'msg':'user:%s register successfully'%user_dic['name']}
    common.send_back(back_dic,conn)

def login(user_dic,conn):
    user=models.User.select_one(name=user_dic['name'])
    if user:
        if user.user_type==user_dic['user_type']:
            if user.password==user_dic['password']:
                session=common.get_session(user_dic['name'])
                user_data.mutex.acquire()
                if user_dic['addr'] in user_data.alive_user:
                    user_data.alive_user.pop(user_dic['addr'])
                user_data.alive_user[user_dic['addr']]=[session,user.id]
                user_data.mutex.release()
                back_dic={'flag':True,'msg':'user:%s login successfully'%user_dic['name'],'session':session,'is_vip':user.is_vip}
                if user_dic['user_type']=='user':
                    back_dic['notice']=user_interface.check_notice_by_count(1)
            else:
                back_dic={'flag':False,'msg':'password differ'}
        else:back_dic={'flag':False,'msg':'user type error'}
    else:
        back_dic={'flag':False,'msg':'username does not exist'}
    common.send_back(back_dic,conn)



