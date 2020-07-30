from lib import common
from db import models
import datetime


# 购买会员接口
@common.login_auth
def charge_vip_interface(recv_dict, conn):
    # 对当前用户的Is_vip字段修改为1  0：普通用户，1：会员
    user_id = recv_dict.get('user_id')
    user_obj = models.User.orm_select(u_id=user_id)[0]

    user_obj.is_vip = 1
    # 更新
    user_obj.orm_update()
    # 发送
    send_dict = {'flag': True, 'msg': '会员充值成功！'}
    common.send_dict(send_dict, conn)


# 下载电影接口
@common.login_auth
def download_movie_interface(recv_dict, conn):
    movie_id = recv_dict.get('movie_id')
    movie_obj = models.Movie.orm_select(m_id=movie_id)[0]

    # 获取当前id的电影名称
    movie_name = movie_obj.movie_name
    # 获取当前电影大小
    movie_size = movie_obj.movie_size
    # 获取服务器电影路径
    movie_path = movie_obj.movie_path

    # 把数据做成字典，发送给客户端
    send_dict = {
        'flag': True,
        'movie_name': movie_name,
        'movie_size': movie_size
    }
    common.send_dict(send_dict, conn)
    # 开始发送电影,流水发送
    with open(movie_path, 'rb') as f:
        for line in f:
            conn.send(line)

    # 记录下载的电影
    record_obj = models.DownloadRecord(
        movie_id=movie_id,
        user_id=recv_dict.get('user_id'),
        download_time=datetime.datetime.now()
    )
    # 插入数据
    record_obj.orm_insert()


# 查看下载记录接口
@common.login_auth
def check_record_interface(recv_dict, conn):
    '''
    只能查看自己的下载记录
    1.获取当前用户的id
    2.查询当前用户id的记录
    '''
    user_id = recv_dict.get('user_id')
    # 查询--->[obj,obj,obj]
    record_list_obj = models.DownloadRecord.orm_select(user_id=user_id)
    # 如果没有记录
    if not record_list_obj:
        send_dic = {
            'flag': False,
            'msg': '下载记录为空!'
        }
    else:
        record_list = []
        for record_obj in record_list_obj:
            # 因为记录表中没有电影名字，所有1.拿到电影id，2.去电影表中拿到名字
            # 1.获取id
            movie_id = record_obj.movie_id
            # 2.根据id去电影表中获取电影对象
            movie_obj = models.Movie.orm_select(m_id=movie_id)[0]
            # 3.根据对象拿到电影名字
            movie_name = movie_obj.movie_name
            # 拿到下载记录表中的下载时间
            download_time = record_obj.download_time
            # 把需要展示给用户的信息添加到列表中
            record_list.append(
                [movie_name, str(download_time)]
            )

        send_dic = {
            'flag': True,
            'record_list': record_list
        }
    common.send_dict(send_dic, conn)


# 查看公告接口
# @common.login_auth
def check_notice_interface(recv_dict, conn):
    notice_list_obj = models.Notice.orm_select()
    notice_list = []

    for notice_obj in notice_list_obj:
        title = notice_obj.title
        content = notice_obj.content
        create_time = notice_obj.create_time

        notice_list.append(
            [title, content, create_time]
        )

    if notice_list:

        send_dict = {'flag': True, 'notice_list': notice_list}
    else:
        send_dict = {'flag': False, 'msg': '还没有公告！'}

    common.send_dict(send_dict, conn)



































































