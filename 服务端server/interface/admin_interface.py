from conf import setting
import os
import datetime
from db.models import Movie, Notice
from lib import common


# 上传电影接口
@common.login_auth
def upload_movie_interface(recv_dict, conn):
    # 服务端获取电影名字
    movie_name = recv_dict.get('movie_name')
    # time = datetime.datetime.now()
    movie_path = os.path.join(setting.MOVIE_FILES_PATH, movie_name)
    # 电影后面拼接时间,文件名字不能有冒号。命名规范
    time = str(datetime.datetime.now()).replace(':', '-')
    movie_name = f'{movie_name}--{time}'
    # 服务端获取电影的大小
    movie_size = recv_dict.get('movie_size')
    recv_data = 0
    # 开始接收电影文件数据
    with open(movie_path, 'wb') as f:
        while recv_data < movie_size:
            data = conn.recv(1024)
            f.write(data)
            recv_data += len(data)

    # 保存电影数据到MySQL中
    movie_obj = Movie(
        movie_name=movie_name,
        movie_size=movie_size,
        movie_path=movie_path,
        is_free=recv_dict.get('is_free'),
        user_id=recv_dict.get('user_id'),
        # 用来校验电影是否已存在
        movie_md5=recv_dict.get('movie_md5'),
        upload_time=datetime.datetime.now(),
        is_delete=0
    )

    movie_obj.orm_insert()

    send_dic = {'flag': True, 'msg': f'电影[{movie_name}]上传成功'}

    common.send_dict(send_dic, conn)


# 删除电影接口
@common.login_auth
def delete_movie_interface(recv_dict, conn):
    movie_id = recv_dict.get('movie_id')

    movie_obj = Movie.orm_select(m_id=movie_id)[0]   # [obj]

    movie_obj.is_delete = 1   # 0未删除，1删除
    # 更新数据
    movie_obj.orm_update()

    # 发送反馈字典
    send_dict = {'flag': True,
                 'msg': f'电影【{movie_obj.movie_name}】删除成功!'}
    common.send_dict(send_dict, conn)


# 发布公告接口
@common.login_auth
def send_notice_interface(recv_dict, conn):
    notice_obj = Notice(
        title=recv_dict.get('title'),
        content=recv_dict.get('content'),
        create_time=str(datetime.datetime.now()),
        user_id=recv_dict.get('user_id')
    )
    # 插入数据库
    notice_obj.orm_insert()
    # 发送反馈信息给客户端
    send_dict = {'flag': True, 'msg': f'【{notice_obj.title}】公告发布成功！'}
    common.send_dict(send_dict, conn)
















































