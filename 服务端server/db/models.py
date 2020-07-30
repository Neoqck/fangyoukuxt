from orm_control.ORM import Models, Integer, String


# 用户表类
class User(Models):
    '''
    u_id: 用户id
    username: 用户名
    password: 用户密码
    user_type :用户类型（管理员、普通）
    is_vip :是否VIP 0表示普通用户，1表示VIP
    register_time :注册时间
    '''
    u_id = Integer(name='u_id', primary_key=True)
    username = String(name='username')
    password = String(name='password')
    user_type = String(name='user_type')
    is_vip = Integer(name='is_vip')
    register_time = String(name='register_time')


# 电影表类
class Movie(Models):
    '''
    m_id :电影id
    movie_name ：电影名字
    movie_size ：电影大小
    movie_path ：电影路径
    is_free ：是否免费  0：免费  1 收费
    user_id ：上传用户Id
    movie_md5 ：电影唯一标识
    upload_time ：上传时间
    is_delete ：是否删除   0 未删除   1删除
    '''
    m_id = Integer(name='m_id', primary_key=True)
    movie_name = String(name='movie_name')
    movie_size = String(name='movie_size')
    movie_path = String(name='movie_path')
    is_free = Integer(name='is_free')
    user_id = Integer(name='user_id')
    movie_md5 = String(name='movie_md5')
    upload_time = String(name='upload_time')
    is_delete = Integer(name='is_delete')


# 公告表类
class Notice(Models):
    '''
    n_id :id
    title :公告标题
    content ： 公告内容
    create_time ：发布时间
    u_id ：发布用户id
    '''
    n_id = Integer(name='n_id', primary_key=True)
    title = String(name='title')
    content = String(name='content')
    create_time = String(name='create_time')
    user_id = Integer(name='user_id')


# 下载记录表
class DownloadRecord(Models):
    '''
    d_id :id
    movie_id :下载的电影id
    user_id :下载用户的id
    download_time :下载时间
    '''
    d_id = Integer(name='d_id', primary_key=True)
    movie_id = Integer(name='movie_id')
    user_id = Integer(name='user_id')
    download_time = String(name='download_time')
























































