from core import admin,user

func_dic={'1':admin.run,'2':user.run}

def run():
    while True:
        print('''
            1.管理员视图
            2.用户视图
        ''')
        choice=input('please choice>>:').strip()
        if choice=='q':break
        if choice not in func_dic:continue
        func_dic[choice]()