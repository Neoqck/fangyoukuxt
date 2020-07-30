from orm_control.mysql_control import MySQL


class Field:
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default


class String(Field):
    def __init__(self, name, column_type='varchar(64)', primary_key=False, default=None):
        super().__init__(name, column_type, primary_key, default)


class Integer(Field):
    def __init__(self, name, column_type='int', primary_key=False, default=None):
        super().__init__(name, column_type, primary_key, default)


class OrmMetaClass(type):
    '''
    1.控制有且只有一个主键
    2.给类的名称空间添加表名，主键名、字段对象
    3.一张表必须要有表名
    '''
    def __new__(cls, class_name, class_bases, class_dict):
        # 过滤Models类，不能控制Models
        if class_name == 'Models':
            return type.__new__(cls, class_name, class_bases, class_dict)

        table_name = class_dict.get('table_name', class_name)   # 此处class_name为默认值

        primary_key = None
        mappings = {}   # 字段名，与字段对象字典
        for key, value in class_dict.items():
            # 过滤非字段
            if isinstance(value, Field):
                mappings[key] = value

                # 下面判断一个表有且只有一个主键
                if value.primary_key:
                    if primary_key:
                        raise TypeError('一张表只能有一个主键！')
                    primary_key = value.name

        if not primary_key:
            raise TypeError('必须有一个主键！')
        # 过滤掉类名称空间中重复的字段
        for key in mappings.keys():
            class_dict.pop(key)

        # 给类的名称空间添加表名，主键、字段名，与字段对象字典
        class_dict['table_name'] = table_name
        class_dict['primary_key'] = primary_key
        class_dict['mappings'] = mappings

        return type.__new__(cls, class_name, class_bases, class_dict)


class Models(dict, metaclass=OrmMetaClass):
    #  对象点属性没有的时候触发，让对象可以点到属性
    def __getattr__(self, item):
        return self.get(item)

    # 赋值的时候触发
    def __setattr__(self, key, value):
        self[key] = value

    # 查询方法
    @classmethod
    def orm_select(cls, **kwargs):
        # 调用MySQL生成游标对象
        mysql = MySQL()
        if not kwargs:
            sql = 'select * from %s' % cls.table_name
            res = mysql.select(sql)
        else:
            # kwargs是一个字典，所有这里的key是第一个字段名，id，value是id对应的值
            key = list(kwargs.keys())[0]
            value = kwargs.get(key)

            # 条件查询
            sql = 'select * from %s where %s = ?' % (cls.table_name, key)
            sql = sql.replace('?', '%s')
            # 用游标对象提交--->接收返回值为[{}]字典套列表
            res = mysql.select(sql, value)

        # 列表生成式
        return [cls(**d) for d in res]


    # 插入方法
    def orm_insert(self):
        # 拿到游标对象
        mysql = MySQL()
        # 除主键字段名
        keys = []
        # 除主键字段值
        values = []
        # 存方？号，有几个字段就存几个问号。替换和%s占位
        args = []
        for key, value in self.mappings.items():
            # 过滤掉主键，主键自增
            if not value.primary_key:
                keys.append(value.name)
                # 存主键以外的字段值，若值没有，则使用默认值
                values.append(getattr(self, value.name, value.default))
                args.append('?')

        # insert into table_name (v1,v2,v3)values(?,?,?)
        sql = 'insert into %s(%s) values(%s)' % (
            self.table_name,
            ','.join(keys),
            ','.join(args)
        )
        # sql: insert into table_name(v1, v2, v3) values(%s, %s, %s)
        sql = sql.replace('?', '%s')

        mysql.execute(sql, values)


    # 更新方法
    def orm_update(self):
        # 拿到游标对象
        mysql = MySQL()
        # 字段名
        keys = []
        # 字段值
        values = []
        # 主键
        primary_key = None

        for key, value in self.mappings.items():
            if value.primary_key:
                primary_key = value.name + '= %s' % getattr(self, value.name)
            else:
                keys.append(value.name + '=?')
                values.append(getattr(self, value.name))

        sql = 'update %s set %s where %s' % (
            self.table_name,
            ','.join(keys),
            primary_key
        )
        sql = sql.replace('?', '%s')
        mysql.execute(sql, values)




































