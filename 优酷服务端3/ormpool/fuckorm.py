from ormpool import mysql_pool

class Field:
    def __init__(self,name,column_type,primary_key,default):
        self.name=name
        self.column_type=column_type
        self.primary_key=primary_key
        self.default=default
class StringField(Field):
    def __init__(self,name=None,column_type='varchar(255)',primary_key=False,default=None):
        super().__init__(name,column_type,primary_key,default)
class IntegerField(Field):
    def __init__(self,name=None,column_type='int',primary_key=False,default=0):
        super().__init__(name,column_type,primary_key,default)

class ModelsMetaclass(type):
    def __new__(cls,name,bases,attrs):
        if name=='Models':
            return type.__new__(cls,name,bases,attrs)
        table_name=attrs.get('table_name',None)
        if not table_name:
            table_name=name
        mappings=dict()
        primary_key=None
        for k,v in attrs.items():
            if isinstance(v,Field):
                mappings[k]=v
                if v.primary_key:
                    if primary_key:
                        raise TypeError('主键重复')
                    primary_key=k
        for k in mappings:
            attrs.pop(k)
        if not primary_key:
            raise TypeError('没有设置主键')
        attrs['table_name']=table_name
        attrs['primary_key']=primary_key
        attrs['mappings']=mappings
        return type.__new__(cls,name,bases,attrs)

class Models(dict,metaclass=ModelsMetaclass):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    def __setattr__(self, key, value):
        self[key]=value
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError('没有该属性')
    @classmethod
    def select_one(cls,**kwargs):
        ms=mysql_pool.Mysql()
        key=list(kwargs.keys())[0]
        value=kwargs[key]
        sql="select * from %s where %s=?"%(cls.table_name,key)
        sql=sql.replace('?','%s')
        res=ms.select(sql,value)
        if res:
            return cls(**res[0])
        else:return None
    @classmethod
    def select_all(cls,**kwargs):
        ms = mysql_pool.Mysql()
        if kwargs:
            key = list(kwargs.keys())[0]
            value = kwargs[key]
            sql = "select * from %s where %s=?" % (cls.table_name, key)
            sql = sql.replace('?', '%s')
            res = ms.select(sql, value)
        else:
            sql="select * from %s"%cls.table_name
            res=ms.select(sql)
        return [cls(**r) for r in res]
    def save(self):
        ms=mysql_pool.Mysql()
        field=[]
        params=[]
        args=[]
        for k,v in self.mappings.items():
            field.append(v.name)
            params.append('?')
            args.append(getattr(self,v.name,v.default))
        sql="insert into %s(%s) values(%s)"%(self.table_name,','.join(field),','.join(params))
        sql=sql.replace('?','%s')
        ms.execute(sql,args)
    def update(self):
        ms=mysql_pool.Mysql()
        field=[]
        args=[]
        pr=None
        for k,v in self.mappings.items():
            if v.primary_key:
                pr=getattr(self,v.name)
            else:
                field.append(v.name+'=?')
                args.append(getattr(self,v.name,v.default))
        sql="update %s set %s where %s=%s"%(self.table_name,','.join(field),self.primary_key,pr)
        sql=sql.replace('?','%s')
        ms.execute(sql,args)

