import pymysql


class MySQL:
    __instance = None

    # 单例模式
    @classmethod
    def singleton(cls):
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        self.mysql_client = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='wdl188638',
            db='youku',
            charset='utf8',
            autocommit=True,
        )
        # 游标对象，以字典形式返回
        self.cursor = self.mysql_client.cursor(pymysql.cursors.DictCursor)

    # 自定义查询方法
    def select(self, sql, args=None):
        # 提交sql语句
        # select * from table where id = %s
        self.cursor.execute(sql, args)

        # 获取返回值,[{},{}]字典套列表，每一个字典是数据库每一行记录
        res = self.cursor.fetchall()
        return res

    # 自定义提交sql语句方法
    def execute(self, sql, args):
        try:
            self.cursor.execute(sql, args)
        except Exception as e:
            print(e)

    # 自定义关闭
    def close(self):
        # 先关闭游标，再关闭数据库连接
        self.cursor.close()
        self.mysql_client.close()




































