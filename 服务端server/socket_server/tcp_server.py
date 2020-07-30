import socket
from conf import setting
from concurrent.futures import ThreadPoolExecutor
import struct
import json
from interface import common_interface, admin_interface, user_interface


server = socket.socket()
server.bind((setting.ip, setting.port))
server.listen(5)
pool = ThreadPoolExecutor(10)


func_dict = {
    # 注册接口
    'register': common_interface.register_interface,
    # 登录接口
    'login': common_interface.login_interface,
    # 检测电影是否存在接口
    'check_movie': common_interface.check_movie_interface,
    # 上传接口
    'upload_movie': admin_interface.upload_movie_interface,
    # # 获取电影列表接口(未删除全部，未删除免费，未删除收费)
    'get_movie_list': common_interface.get_movie_list_interface,
    # 删除电影接口
    'delete_movie': admin_interface.delete_movie_interface,
    # 发布公告接口
    'send_notice': admin_interface.send_notice_interface,
    # 购买会员接口
    'charge_vip': user_interface.charge_vip_interface,
    # 下载电影接口
    'download_movie': user_interface.download_movie_interface,
    # 查看下载记录
    'check_record': user_interface.check_record_interface,
    # 查看公告接口
    'check_notice': user_interface.check_notice_interface,
}


def run():
    print('---启动服务端---')
    while True:
        conn, addr = server.accept() # 允许连接
        print('连接成功！')
        pool.submit(working, conn, addr) # 异步提交


# 异步回调函数
def working(conn, addr):
    while True:
        try:
            # 1.接收报头
            hander = conn.recv(4)
            # 2.解开字典，获取字典长度
            dict_len = struct.unpack('i', hander)[0]
            # 3.接收真实json格式字典数据的长度
            json_dict = conn.recv(dict_len)
            # 4.解开json,解开二进制,获取原始真实字典
            recv_dict = json.loads(json_dict.decode('utf-8'))
            # 5.把addr添加到字典中
            recv_dict['addr'] = str(addr)

            # 调用任务分发函数：对任务进行分发
            dispacher(recv_dict, conn)
        except Exception as e:
            print(e)
            conn.close()
            break


# 任务分发
def dispacher(recv_dict, conn):
    type = recv_dict.get('type')  # 获取字典传过来的功能函数名字
    if type in func_dict:
        func_dict.get(type)(recv_dict, conn)






























































