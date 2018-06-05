from ormpool.fuckorm import Models,StringField,IntegerField

class User(Models):
    table_name='userinfo'
    id=IntegerField('id',primary_key=True)
    name=StringField('name')
    password=StringField('password')
    is_vip=IntegerField('is_vip')
    locked=IntegerField('locked')
    user_type=StringField('user_type')
    create_time=StringField('create_time')

class Movie(Models):
    table_name='movie'
    id=IntegerField('id',primary_key=True)
    name=StringField('name')
    path=StringField('path')
    is_free=IntegerField('is_free')
    is_delete=IntegerField('is_delete')
    file_md5=IntegerField('file_md5')
    file_size=IntegerField('file_size')
    create_time=StringField('create_time')
    user_id=IntegerField('user_id')

class Notice(Models):
    table_name='notice'
    id=IntegerField('id',primary_key=True)
    name=StringField('name')
    content=StringField('content')
    create_time=StringField('create_time')
    user_id=IntegerField('user_id')

class DownloadRecord(Models):
    table_name='download_record'
    id=IntegerField('id',primary_key=True)
    user_id=IntegerField('user_id')
    movie_id=IntegerField('movie_id')
    create_time=StringField('create_time')
