from core import admin
from core import user


func_dict = {
    '1': admin.admin_view,
    '2': user.user_view
}


def run():
    while True:
        print('---欢迎来到王氏电影家族---')

        print('''
        优酷系统：
        1.管理员视图
        2.普通用户视图
        q.退出
        ''')
        choice = input('请选择功能：').strip()
        if choice == 'q':
            break
        if choice not in func_dict:
            print('选择的功能有误！请重新选择！')
            continue
        func_dict[choice]()






