import json
import struct
import os
from conf import setting
import hashlib
from core.user import user_info



# 客户端发送并接受消息
def send_and_recv(send_dict, client, file=None):
    '''
    :param send_dict: 用户字典信息
    :param client: 拿到socket客户端对象
    :param file:  电影路径，证明有没有上传的文件。比如注册没有上传文件，只有用户字典信息
    :return: recv_dict: 解码之后的真实字典数据
    '''
    # 客户端往服务端发送数据
    # 1. 字典转成json格式
    json_dict = json.dumps(send_dict).encode('utf-8')
    # 2. 制作报头
    hander = struct.pack('i', len(json_dict))
    # 3. 发送报头
    client.send(hander)
    # 4. 发送json字典
    client.send(json_dict)

    # 判断是否有电影文件
    if file:
        with open(file, 'rb') as f:
            # 循环发送
            for line in f:
                client.send(line)

    # 客户端接收服务端返回的数据
    # 1. 接收报头
    hander = client.recv(4)
    # 2. 解析，得到字典长度
    dict_len = struct.unpack('i', hander)[0]
    # 3. 接收json格式的字典
    dict_json = client.recv(dict_len)
    # 4. 解开json,解码二进制，得到原始真正字典
    recv_dict = json.loads(dict_json.decode('utf-8'))

    return recv_dict


# 获取电影列表
def get_movie_list():
    movie_list = os.listdir(setting.UPLOAD_MOVIE_PATH)
    return movie_list


# 获取电影md5值
def get_movie_md5(movie_path):
    md5 = hashlib.md5()
    # 获取电影大小，用来对电影的数据进行截取
    movie_size = os.path.getsize(movie_path)
    # 截取部分的位置
    # [电影开头，电影1/4，电影1/2，电影结尾]
    bytes_list = [0, movie_size//4, movie_size//2, movie_size -10]

    with open(movie_path, 'rb') as f:
        for line in bytes_list:
            # 光标移动到指定位置
            f.seek(line)
            # 每个位置获取10个bytes
            data = f.read(10)
            # 生成md5值，加密
            md5.update(data)
    return md5.hexdigest()


# 装饰器
def outter(func):
    from core.admin import user_info
    from core.user import user_info
    def inner(*args, **kwargs):

        if user_info.get('cookies'):
            return func(*args, **kwargs)
        else:
            from core import admin
            from socket_client import tcp_client
            print('请先登录！')
            admin.login(tcp_client.get_client())
    return inner


# 下载免费收费电影
def download_movie(client, is_pay):
    while True:
        # 获取所有电影列表
        send_dict = {
            'type': 'get_movie_list',
            'cookies': user_info.get('cookies'),
            # 获取电影的类型
            'movie_type': is_pay
        }
        recv_dict = send_and_recv(send_dict, client)

        free_movie_list = recv_dict.get('movie_list')
        # 判断是否有电影
        if free_movie_list:
            for index, movie_list in enumerate(free_movie_list):
                print(index, movie_list)

            # 用户选择
            choice = input('输入下载的电影编号(q.退出):').strip()
            if choice == 'q':
                break

            if not choice.isdigit():
                print('输入不规范！')
                continue
            choice = int(choice)
            if choice not in range(len(free_movie_list)):
                print('输入不在范围！')
                continue
            # 获取选择的电影id [名字，id,免费]
            # free_movie_list = [['在线发牌——2019-12-22 20:46:57.821142', 15, '免费']]
            movie_list_id = free_movie_list[choice][1]
            send_dict = {
                'type': 'download_movie',
                'cookies': user_info.get('cookies'),
                'movie_id': movie_list_id
            }
            # 发送
            recv_dict = send_and_recv(send_dict, client)
            # 判断电影是否存在
            if recv_dict.get('flag'):
                # 获取电影名称
                movie_name = recv_dict.get('movie_name')
                # 获取电影大小
                movie_size = recv_dict.get('movie_size')
                # 拼接下载电影存放目录
                movie_path = os.path.join(setting.DOWNLOAD_MOVIE_PATH, movie_name)

                # 开始接收数据
                recv_data = 0
                with open(movie_path, 'wb') as f:
                    while recv_data < int(movie_size):
                        data = client.recv(1024)
                        f.write(data)
                        recv_data += len(data)
                print(f'电影【{movie_name}】下载成功！')
                break
            else:
                print('没有可下载的电影！')
                break
        else:
            print('没有电影！')
            break












































