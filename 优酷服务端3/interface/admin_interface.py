import os
from conf import settings
from lib import common
from db import models


@common.login_auth
def upload_movie(user_dic,conn):
    recv_size=0
    file_name=common.get_session(user_dic['file_name'])+user_dic['file_name']
    path=os.path.join(settings.BASE_MOVIE_LIST,file_name)
    with open(path,'wb')as f:
        while recv_size<user_dic['file_size']:
            data=conn.recv(1024)
            f.write(data)
            recv_size+=len(data)
    movie=models.Movie(name=file_name,path=path,user_id=user_dic['user_id'],file_size=user_dic['file_size'],file_md5=user_dic['file_md5'],
                       is_free=user_dic['is_free'])
    movie.save()
    back_dic={'flag':True,'msg':'movie:%s upload successfully'%(user_dic['file_name'])}
    common.send_back(back_dic,conn)

@common.login_auth
def delete_movie(user_dic,conn):
    movie=models.Movie.select_one(id=user_dic['movie_id'])
    movie.is_delete=1
    movie.update()
    back_dic={'flag':True,'msg':'movie:%s delete successfully'%movie.name}
    common.send_back(back_dic,conn)

@common.login_auth
def release_notice(user_dic,conn):
    notice=models.Notice(name=user_dic['name'],content=user_dic['content'],user_id=user_dic['user_id'])
    notice.save()
    back_dic={'flag':True,'msg':'notice:%s release successfully'%user_dic['name']}
    common.send_back(back_dic,conn)

@common.login_auth
def check_movie(user_dic,conn):
    movie=models.Movie.select_one(file_md5=user_dic['file_md5'])
    if movie:
        back_dic={'flag':True,'msg':'该影片已存在'}
    else:
        back_dic={'flag':False,'msg':'该影片不存在，可以上传'}
    common.send_back(back_dic,conn)