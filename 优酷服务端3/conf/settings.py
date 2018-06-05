import os
host='127.0.0.1'
port=3306
user='root'
password='123'
database='youku'
charset='utf8'
autocommit=True

BASE_DIR=os.path.dirname(os.path.dirname(__file__))
BASE_MOVIE_LIST=os.path.join(BASE_DIR,'movie_list')
server_address=('127.0.0.1',8081)