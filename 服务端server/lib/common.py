import json
import struct
import hashlib
import uuid


# 发送消息的功能
def send_dict(send_dict, conn):
    # 1.将字典转成json,二进制格式
    json_dict = json.dumps(send_dict).encode('utf-8')
    # 2.制作报头
    hander_dict = struct.pack('i', len(json_dict))
    # 3.发送报头
    conn.send(hander_dict)
    # 4.发送json字典
    conn.send(json_dict)


# 加密
def md5(pwd):
    md5 = hashlib.md5()
    value = '王氏家族终极密码'
    md5.update(value.encode('utf-8'))
    md5.update(pwd.encode('utf-8'))
    return md5.hexdigest()


# 生成session随机字符串
def get_session():
    md5 = hashlib.md5()
    value = str(uuid.uuid4())
    md5.update(value.encode('utf-8'))
    return md5.hexdigest()


# 登录认证装饰器
def login_auth(func):
    from db.session_data import session_dict
    # args-->func-->upload_movie(recv_dict,coon)
    def inner(*args, **kwargs):
        # 获取客户端的cookies值
        client_cookies = args[0].get('cookies')  # None 用户没有登录  有值：已登录
        # 从back_dict中获取客户端addr，拿到addr去获取存在服务端的session值
        addr = args[0].get('addr')
        # 判断客户端cookies有值
        if client_cookies:
            # 在判断客户端cookies和服务端session值是否相等
            server_session = session_dict.get(addr)[0]  # [0]存的式session值，[1]存的是用户id
            if server_session == client_cookies:
                # 将服务端存的用户id添加到客户端发过来的字典中
                # recv_dict['user_id'] = [session, user_id][1]
                args[0]['user_id'] = session_dict.get(addr)[1]
                return func(*args, **kwargs)  # 原路执行
            else:
                send_dic = {'flag': False, 'msg': '同一个用户不能多台电脑同时登录！'}
                # 拿到conn
                conn = args[1]
                # 发送反馈信息到服务端   # 个人总结，应该是发送到客户端
                send_dict(send_dic, conn)
        else:
            send_dic = {'flag': False, 'msg': '请先登录！'}
            # 拿到conn
            conn = args[1]
            # 发送反馈信息到服务端	  # 个人总结，应该是发送到客户端
            send_dict(send_dic, conn)

    return inner


























































