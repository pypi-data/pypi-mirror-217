import time
from decimal import Decimal
from config import DB_CONF
from db_test import create_truncate_table
from mysqlx import db
from mysqlx.orm import DelFlag
from test.models import User
from mysqlx.snowflake import init_snowflake
from datetime import datetime


def full_test():
    create_truncate_table('user')

    # ------------------------------------------------测试实例方法 ------------------------------------------------
    u = User(name='张三', age=55, birth_date='1968-10-08', sex=0, grade=1.0, point=20.5, money=Decimal(854.56))
    rowcount = u.persist()
    assert rowcount > 0, 'persist'
    User.delete_by('where id > ?', 0)
    id = u.inst_save()
    assert User.count(name='张三') == 1, 'Count not eq 1'
    u1 = User(id=id, sex=1)
    u2 = u1.load('name', 'age')
    print(u1)
    print(u2)
    u1.load()
    print(u1)
    assert u1 == u2, 'u1 not eq u2'

    u1.name = '李四'
    u1.update()
    u3 = User.find_by_id(id, 'id', 'name')
    assert u3.name == '李四', 'update '

    u3.logical_delete()
    u4 = User.find_by_id(id)
    assert User.count() == 1, 'delete'
    assert u4.del_flag == 1, 'delete'

    u4.delete()
    assert User.count() == 0, 'delete'

    # ------------------------------------------------测试静态方法------------------------------------------------------
    rowcount = User.insert(name='张三', age=55, birth_date='1968-10-08', sex=0, grade=1.0, point=20.5, money=Decimal(854.56))
    assert rowcount == 1, 'insert'

    user = User.create(name='李四', age=55, birth_date='1968-10-08', sex=0, grade=1.0, point=20.5, money=Decimal(854.56))
    id2 = user.id
    assert id2 > 0, 'create'

    User.update_by_id(id2, name='王五')
    u5 = User.find_by_id(id2, 'name')
    assert u5.name == '王五', 'update_by_id'
    u5 = User.query_by_id(id2, 'name')
    assert u5['name'] == '王五', 'query_by_id'
    u5 = User.select_by_id(id2, 'name', 'age', 'create_time')
    print(u5)

    User.logical_delete_by_id(id2)
    u6 = User.find_by_id(id2, 'del_flag')
    assert u6.del_flag == 1, 'logic_delete_by_id'
    User.un_logical_delete_by_id(id2)
    u6 = User.find_by_id(id2, 'del_flag')
    assert u6.del_flag == 0, 'logic_delete_by_id'

    User.update_by_id(id2, del_flag=0)
    u7 = User.find_by_id(id2, 'del_flag')
    assert u7.del_flag == 0, 'update_by_id'

    users = User.find(name='王五')
    assert len(users) == 1, 'find'
    users = User.query(name='王五')
    assert len(users) == 1, 'query'
    users = User.select(name='王五')
    assert len(users) == 1, 'select'
    users = User.find('id', 'name', limit=2)
    assert len(users) == 2, 'find'
    ids = [user.id for user in users]
    User.logical_delete_by_ids(ids=ids, batch_size=1)
    users2 = User.find_by_ids(ids, 'del_flag')
    assert len(users2) == 2, 'logic_delete_by_ids'
    for user in users2:
        assert user.del_flag == DelFlag.DELETED.value, 'logic_delete_by_ids'

    User.un_logical_delete_by_ids(ids=ids, update_by=11)
    users2 = User.find_by_ids(ids, 'del_flag')
    assert len(users2) == 2, 'un_logical_delete_by_ids'
    for user in users2:
        assert user.del_flag == DelFlag.UN_DELETE.value, 'logic_delete_by_ids'

    User.delete_by_id(id2)
    assert User.count() == 1, 'delete_by_id'

    User.delete_by_ids(ids)
    assert User.count() == 0, 'delete_by_ids'


def get_attr():
    user = User(id=1, name='张三', age=41)
    user.logic_delete_by_id(1)


if __name__ == '__main__':
    db.init_db(**DB_CONF)
    init_snowflake(epoch=int(time.mktime(time.strptime("2023-6-26 00:00:00", '%Y-%m-%d %H:%M:%S')) * 1000))
    full_test()

    users = User.find('id', 'name', 'grade', 'create_time', id='in(1,4)', name="like '张三%'", grade='>=1', create_time="between '2023-06-07 10:48:01' and '2023-06-07 10:48:06'")
    for user in users:
        print(user)
    users = User.find()
    for user in users:
        print(user)


    # kwargs = {
    #     'name': '张三',
    #     'age': 18,
    #     'sex': 0
    # }
    # table = 'user'
    # cols, args = zip(*kwargs.items())
    # sql = 'INSERT INTO `%s` (%s) VALUES (%s)' % (table, ','.join(['`%s`' % col for col in cols]), ','.join(['%' + '(%s)' % col + 's' for col in cols]))
    # print(sql)

    # cls = User.__class__
    # user = cls(('test', Model, kwargs))
    # print(User)

    # for user in User.find():
    #     print(user)

    now = datetime.now()
    User.batch_insert(*[{'name': '王五', 'age': 55, 'birth_date': '1968-10-08', 'sex': 0, 'grade': 1.0, 'point': 20.5, 'money': 854.56, 'create_time': now},
                       {'name': '赵六', 'age': 55, 'birth_date': '1968-10-08', 'sex': 0, 'grade': 1.0, 'point': 20.5, 'money': 854.56, 'create_time': now}])

    for u in User.query():
        print(u)

    for u in User.select_page_by(2, 3, 'where name=?', '张三'):
        print(u)

    for u in User.find_page_by(2, 3, 'where name=?', '张三'):
        print(u)

    for u in User.query_page(2,3):
        print(u)

    for u in User.find_page(2,3):
        print(u)

    rowcount = User.delete_by('where name=? and age=?', '张三', 55)
    print(rowcount)

    cnt = User.count_by('where name=?', '李四')
    print(cnt)

    for u in User.query_by('select id, name, age from user where name=?', '张三'):
        print(u)

    User.query(limit=(2, 3))

