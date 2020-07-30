from db import models
import datetime
from lib import common
from threading import Lock
from db.session_data import session_dict


# 公共锁
mutex = Lock()


# 注册
def register_interface(recv_dict, conn):
    username = recv_dict.get('username')
    # 1.判断用户是否存在 ---接收到--->[{},{}]  列表套字典
    user_obj_list = models.User.orm_select(username=username)

    # 2.有值--->用户存在
    if user_obj_list:
        send_dict = {'flag': False, 'msg': '用户已存在'}
    # 3.没有值就注册
    else:
        user_obj = models.User(
            username=username,
            password=common.md5(recv_dict.get('password')),
            user_type=recv_dict.get('user_type'),
            is_vip=0,
            register_time=datetime.datetime.now()
        )
        user_obj.orm_insert()
        send_dict = {'flag': True, 'msg': '注册成功！'}
        print(f'【{username}】用户注册成功！')
    # 调用公共方法发送数据到客户端
    common.send_dict(send_dict, conn)


# 登录
def login_interface(recv_dict, conn):
    # 1.判断用户是否存在
    username = recv_dict.get('username')
    # 1.判断用户是否存在 ---接收到--->[{}]  列表套字典
    user_obj_list = models.User.orm_select(username=username)

    # 2.没有值--->用户不存在
    if not user_obj_list:
        send_dict = {'flag': False, 'msg': '用户不存在'}
    # 1.用户存在的情况
    else:
        user_obj = user_obj_list[0]
        # 2.判断密码是否正确
        re_password = recv_dict.get('password')  # 用户输入的密码
        re_password = common.md5(re_password)
        mysql_password = user_obj.password   # 数据库存的真正密码

        # 密码正确
        if re_password == mysql_password:
            addr = recv_dict.get('addr')
            mutex.acquire()   # 加锁
            # 用户登录成功后，获取session值
            session = common.get_session()
            # 给session字典添加值   {地址：[session,用户id]}这样session值就是唯一
            session_dict[addr] = [session, user_obj.u_id]
            mutex.release()  # 释放锁

            # 默认不是VIP
            is_vip = False
            if user_obj.is_vip:
                is_vip = True
            send_dict = {'flag': True,
                         'msg': '登录成功！',
                         'session': session,
                         'is_vip': is_vip}

        # 密码不正确
        else:
            send_dict = {'flag': False, 'msg': '密码错误！'}
    # 调用接口发送反馈信息字典
    common.send_dict(send_dict, conn)


# 检测电影是否存在接口
@common.login_auth
def check_movie_interface(recv_dict, conn):
    movie_md5 = recv_dict.get('movie_md5')
    # 校验数据库中电影是否存在--->判断该md5是否存在
    movie_obj_list = models.Movie.orm_select(movie_md5=movie_md5)
    # 若电影不存在，则返回可以上传
    if not movie_obj_list:
        send_dict = {'flag': True, 'msg': '可以上传'}
    # 若电影存在，则返回不可以上传
    else:
        send_dict = {'flag': False, 'msg': '电影已存在！'}
    # 调接口，发送
    common.send_dict(send_dict, conn)


# 获取相应电影接口
@common.login_auth
def get_movie_list_interface(recv_dict, conn):
    # 查询电影表，获取所有电影对象
    movie_obj_list = models.Movie.orm_select()
    movie_list = []
    if movie_obj_list:
        for movie_obj in movie_obj_list:
            # 过滤已删除的电影对象
            if movie_obj.is_delete == 0:
                # 获取所有电影
                if recv_dict.get('movie_type') == 'all':
                    # 电影名称， 电影ID，电影是否免费
                    movie_list.append(
                        [movie_obj.movie_name, movie_obj.m_id,
                         '免费' if movie_obj.is_free == 0 else '收费']
                    )

                elif recv_dict.get('movie_type') == 'free':
                    if movie_obj.is_free == 0:
                        movie_list.append(
                            [movie_obj.movie_name,
                             movie_obj.m_id,
                             '免费'])
                elif recv_dict.get('movie_type') == 'pay':
                    if movie_obj.is_free == 1:
                        movie_list.append(
                            [movie_obj.movie_name,
                             movie_obj.m_id,
                             '收费'])

        if len(movie_list) > 0:
            send_dict = {'flag': True, 'movie_list': movie_list}
            common.send_dict(send_dict, conn)

        if not len(movie_list) > 0:
            send_dict = {'flag': False, 'msg': '还没有电影！'}
            common.send_dict(send_dict, conn)

    else:
        send_dict = {'flag': False, 'msg': '目前还没有电影！'}
        common.send_dict(send_dict, conn)




























































