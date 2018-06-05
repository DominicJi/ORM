import os
from lib import common
from db import models

@common.login_auth
def buy_member(user_dic,conn):
    user=models.User.select_one(id=user_dic['user_id'])
    user.is_vip=1
    user.update()
    back_dic={'flag':True,'msg':'buy successfully'}
    common.send_back(back_dic,conn)

@common.login_auth
def download_movie(user_dic,conn):
    movie=models.Movie.select_one(id=user_dic['movie_id'])
    user=models.User.select_one(id=user_dic['user_id'])
    wait_time = 0
    if user_dic['movie_type']=='free':
        if user.is_vip:
            wait_time=0
        else:
            wait_time=30
    back_dic={'flag':True,'wait_time':wait_time,'file_size':movie.file_size,'file_md5':movie.file_md5,'file_name':movie.name}
    common.send_back(back_dic,conn)
    download_record=models.DownloadRecord(user_id=user_dic['user_id'],movie_id=movie.id)
    download_record.save()
    with open(movie.path,'rb')as f:
        for line in f:
            conn.send(line)

@common.login_auth
def check_download_record(user_dic,conn):
    #record=user_id,movie_id
    record_list=models.DownloadRecord.select_all(user_id=user_dic['user_id'])
    back_movie_list = []
    if record_list:
        for r in record_list:
            movie=models.Movie.select_one(id=r.movie_id)
            back_movie_list.append(movie.name)
        back_dic={'flag':True,'download_list':back_movie_list}
    else:
        back_dic={'flag':False,'msg':'暂无观影记录'}
    common.send_back(back_dic,conn)



@common.login_auth
def check_notice(user_dic,conn):
    notice_list=check_notice_by_count()
    if notice_list:
        back_dic={'flag':True,'notice_list':notice_list}
    else:
        back_dic={'flag':False,'msg':'暂无公告'}
    common.send_back(back_dic,conn)


def check_notice_by_count(count=None):
    notice_list=models.Notice.select_all()
    back_notice_list=[]
    if notice_list:
        if not count:
            for notice in notice_list:
                back_notice_list.append({notice.name:notice.content})
        else:
            new_list=sorted(notice_list,key=lambda notice:notice.create_time)
            last_notice=new_list[-1]
            back_notice_list.append({last_notice.name:last_notice.content})
        return back_notice_list
    else:
        return None




