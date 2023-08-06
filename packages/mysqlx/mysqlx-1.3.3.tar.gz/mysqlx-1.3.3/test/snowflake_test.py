import time
from mysqlx.snowflake import init_snowflake, get_id


if __name__ == '__main__':
    my_epoch = int(time.mktime(time.strptime("2023-6-26 00:00:00", '%Y-%m-%d %H:%M:%S')) * 1000)
    print(my_epoch)
    init_snowflake(epoch=my_epoch)
    for _ in range(20):
        print(get_id())