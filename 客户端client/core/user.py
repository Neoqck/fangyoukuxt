from socket_client import tcp_client
from lib import common


user_info = {'cookies': None}


# 用户注册
def register(client):
    while True:
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()
        re_password = input('确认密码:').strip()
        if not password == re_password:
            print('密码不一致，重新输入！')
            continue
        send_dict = {
            'type': 'register',
            'username': username,
            'password': password,
            'user_type': 'user'
        }
        recv_dict = common.send_and_recv(send_dict, client)
        if recv_dict.get('flag'):
            print(recv_dict.get('msg'))
            user_info['cookies'] = recv_dict.get('session')
            break
        else:
            print(recv_dict.get('msg'))


# 用户登录
def login(client):
    while True:
        username = input('输入用户名：').strip()
        password = input('输入密码').strip()

        send_dict = {
            'type': 'login',
            'username': username,
            'password': password,
            'user_type': 'user'
        }
        recv_dict = common.send_and_recv(send_dict, client)
        if recv_dict.get('flag'):
            print(recv_dict.get('msg'))
            # 登录成功后设置session
            user_info['cookies'] = recv_dict.get('session')
            break
        else:
            print(recv_dict.get('msg'))


# 查看电影
def check_movies(client):
    print('---查看电影---')
    send_dict = {
        'type': 'get_movie_list',
        'cookies': user_info.get('cookies'),
        'movie_type': 'all'
    }
    recv_dict = common.send_and_recv(send_dict, client)
    if recv_dict.get('flag'):
        movie_list = recv_dict.get('movie_list')
        for index, move in enumerate(movie_list):
            print(index, move)
    else:
        print(recv_dict.get('msg'))


# 充值会员
def charge_vip(client):
    while True:
        print('---充值会员---')
        is_vip = input('确认充值VIP(y/n)? :').strip()
        if is_vip == 'n':
            break
        elif is_vip == 'y':
            send_dict = {
                'type': 'charge_vip',
                'cookies': user_info.get('cookies')
            }

            recv_dict = common.send_and_recv(send_dict, client)

        else:
            print('输入不规范！')
            continue
        if recv_dict.get('flag'):
            print(recv_dict.get('msg'))
            break


# 下载免费电影
def download_free_movie(client):
    common.download_movie(client, is_pay='free')


# 下载收费电影
def download_charge_movie(client):
    common.download_movie(client, is_pay='pay')


# 查看下载记录
def check_download_record(client):
    send_dict = {
        'type': 'check_record',
        'cookies': user_info.get('cookies')
    }
    recv_dict = common.send_and_recv(send_dict, client)
    # 判断有无下载记录
    if recv_dict.get('flag'):
        record_list = recv_dict.get('record_list')
        for line in record_list:
            print(line)
    else:
        print(recv_dict.get('msg'))


# 查看公告
def check_notice(client):
    send_dict = {
        'type': 'check_notice',
        'cookies': user_info.get('cookies')
    }
    recv_dict = common.send_and_recv(send_dict, client)
    # 判断有无公告
    if recv_dict.get('flag'):
        notice_list = recv_dict.get('notice_list')  # -->[[],[],[]]
        for line in notice_list:
            print(line)

    else:
        print(recv_dict.get('msg'))


func_dict = {
    '1': register,
    '2': login,
    '3': check_movies,
    '4': charge_vip,
    '5': download_free_movie,
    '6': download_charge_movie,
    '7': check_download_record,
    '8': check_notice
}


def user_view():
    client = tcp_client.get_client()
    while True:
        print('---用户---')
        print('''
        - 1.注册
        - 2.登录
        - 3.查看视频
        - 4.充值会员
        - 5.下载免费视频
        - 6.下载收费视频
        - 7.查看下载记录
        - 8.查看公告
        - q.退出
        ''')

        choice = input('请选择功能：').strip()
        if choice == 'q':
            break
        if choice not in func_dict:
            print('选择的功能有误！请重新选择！')
            continue
        func_dict[choice](client)






























