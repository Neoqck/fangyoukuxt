from socket_client import tcp_client
from lib import common
import os
from conf import setting


user_info = {'cookies': None}

# 管理员注册
def register(client):
    while True:
        user_name = input('请输入用户名：').strip()
        password = input('请输入密码：').strip()
        re_password = input('确认密码：').strip()
        if not password == re_password:
            print('两次密码不一致，重新输入！')
            continue
        send_dict = {
            'type': 'register',
            'username': user_name,
            'password': password,
            'user_type': 'admin'
        }
        recv_dict = common.send_and_recv(send_dict, client)
        if recv_dict.get('flag'):
            print(recv_dict.get('msg'))
            user_info['cookies'] = recv_dict.get('session')
            break
        else:
            print(recv_dict.get('msg'))


# 管理员登录
def login(client):
    while True:
        user_name = input('输入用户名：').strip()
        password = input('输入密码：').strip()

        send_dict = {
            'type': 'login',
            'username': user_name,
            'password': password,
            'user_type': 'admin'
        }
        recv_dict = common.send_and_recv(send_dict, client)
        if recv_dict.get('flag'):
            print(recv_dict.get('msg'))
            # 登录成功后设置session值
            user_info['cookies'] = recv_dict.get('session')
            break
        else:
            print(recv_dict.get('msg'))


# 上传电影
def upload_movie(client):        # 此处需注意，原文函数名应该不对
    while True:
        # 获取上传电影目录中的所有电影，并选择
        movie_list = common.get_movie_list()

        # 若没有可上传的电影
        if not movie_list:
            print('没有可以上传的电影，请先后台添加后上传')
            break

        for index, movie_name in enumerate(movie_list):
            print(index, movie_name)

        choice = input('请选择要上传的电影编号(q.退出)：').strip()
        if choice == 'q':
            break
        if not choice.isdigit():
            print('请输入数字！')
            continue
        choice = int(choice)

        if choice not in range(len(movie_list)):
            print('输入的不在范围，重新输入！')
            continue

        # 电影名字
        movie_name = movie_list[choice]
        # 电影路径
        movie_path = os.path.join(setting.UPLOAD_MOVIE_PATH, movie_name)
        # 获取电影大小
        movie_size = os.path.getsize(movie_path)
        # 获取电影md5值
        movie_md5 = common.get_movie_md5(movie_path)
        # 校验电影是否存在
        send_dict = {
            'type': 'check_movie',
            'cookies': user_info.get('cookies'),
            'movie_md5': movie_md5
        }
        back_dict = common.send_and_recv(send_dict, client)

        if not back_dict.get('flag'):
            print(back_dict.get('msg'))
            continue
        # 确认电影是否免费
        is_free = input('y/n 免费/收费').strip()

        number = 1

        if is_free == 'y':
            number = 0

        # 电影不存在， 发送上传电影请求
        send_dict = {
            'type': 'upload_movie',
            'cookies': user_info.get('cookies'),
            'movie_md5': movie_md5,
            'movie_name': movie_name,
            'movie_size': movie_size,
            'is_free': number
        }

        recv_dict = common.send_and_recv(send_dict, client, file=movie_path)
        if recv_dict.get('flag'):
            print(recv_dict.get('msg'))
            break


# 删除电影
def delete_movie(client):
    while True:
        print('---删除电影---')
        # 1. 获取服务端可以删除的电影
        send_dict = {
            'type': 'get_movie_list',
            'cookies': user_info.get('cookies'),
            'movie_type': 'all'
        }
        recv_dict = common.send_and_recv(send_dict, client)
        if not recv_dict.get('flag'):
            print(recv_dict.get('msg'))
            break
        # 2. 打印可删除的电影
        # movie_list --> [[电影名，ID，收费免费],[],[]]
        movie_list = recv_dict.get('movie_list')

        for index, movie_name in enumerate(movie_list):
            print(index, movie_name)

        choice = input('请输入要删除的电影编号(q.退出):').strip()
        if choice == 'q':
            break
        if not choice.isdigit():
            print('请输入数字！')
            continue
        choice = int(choice)

        if choice not in range(len(movie_list)):
            print('输入不在范围')
            continue

        # 获取电影的id，因为名字可能一样，但是数据库中id是唯一的
        movie_name_id = movie_list[choice][1]
        send_dict = {
            'type': 'delete_movie',
            'cookies': user_info.get('cookies'),
            'movie_id': movie_name_id
        }

        recv_dict2 = common.send_and_recv(send_dict, client)

        if recv_dict2.get('flag'):
            print(recv_dict2.get('msg'))
            break


# 发布公告
def send_notice(client):
    while True:
        title = input('请输入公告标题(15字以内):').strip()
        if len(title) > 15:
            continue
        content = input('输入公告内容(100字以内):')
        if len(content) > 100:
            continue
        send_dict = {
            'type': 'send_notice',
            'cookies': user_info.get('cookies'),
            'title': title,
            'content': content
        }

        recv_dict = common.send_and_recv(send_dict, client)

        if recv_dict.get('flag'):
            print(recv_dict.get('msg'))
            break
        else:
            print(recv_dict.get('msg'))
            break



func_dict = {
    '1': register,
    '2': login,
    '3': upload_movie,
    '4': delete_movie,
    '5': send_notice
}



def admin_view():
    client = tcp_client.get_client()
    while True:
        print('---管理员---')
        print('''
        1.注册
        2.登录
        3.上传视频
        4.删除视频
        5.发布公告
        q.退出
        ''')

        choice = input('请选择功能：').strip()
        if choice == 'q':
            break
        if choice not in func_dict:
            print('选择功能有误，重新选择！')
            continue
        func_dict[choice](client)























































