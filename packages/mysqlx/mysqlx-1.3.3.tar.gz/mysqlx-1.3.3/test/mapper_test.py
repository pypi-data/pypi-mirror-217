from mysqlx import db
from test.mapper import user

if __name__ == '__main__':
    from config import DB_CONF
    # import logging
    # logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]: %(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    db.init_db(**DB_CONF, debug=False)
    args = [
        ('张三', 55, '1968=-10-08', 0, 1.0, 20.5, 854.56),
        ('张三', 55, '1968=-10-08', 0, 1.0, 20.5, 854.56)
    ]
    user.batch_insert(args)

    print(user.select_name(4))

    user.user_update('王五', 5)

    user.user_update2(id=6, name='赵六')

    r = user.select_all()
    for i in r:
        print(i)

    r = user.select_all2()
    for i in r:
        print(i)

    for u in user.select_users('李四'):
        print(u)
