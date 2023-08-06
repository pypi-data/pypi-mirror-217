Install
'''''''

::

   pip install mysqlx

Usage Sample
''''''''''''

::

   CREATE TABLE `user` (
     `id` bigint NOT NULL AUTO_INCREMENT,
     `name` varchar(45) NOT NULL,
     `age` int NOT NULL,
     `birth_date` date DEFAULT NULL,
     `sex` tinyint DEFAULT NULL,
     `grade` float DEFAULT NULL,
     `point` double DEFAULT NULL,
     `money` decimal(8,4) DEFAULT NULL,
     `create_by` bigint DEFAULT NULL,
     `create_time` datetime DEFAULT CURRENT_TIMESTAMP,
     `update_by` bigint DEFAULT NULL,
     `update_time` datetime DEFAULT NULL,
     `del_flag` tinyint NOT NULL DEFAULT '0',
     PRIMARY KEY (`id`)
   ) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


   ----------------------------------------------------------------------------------------

   from mysqlx import db

   db_conf = {
       'host': '127.0.0.1',
       'port': 3306, 
       'user': 'root', 
       'password': 'xxx', 
       'database': 'test',
       'pool_size': 5,
       'show_sql': True
   }

   if __name__ == '__main__':
       db.init_db(**db_conf)
       
       # Return effect rowcount
       rowcount = db.insert('user', name='张三', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
       assert rowcount == 1, '1 effect rowcount'
       assert db.get('select count(1) from user') == 1, 'count is 1'

       # Return primary key
       id2 = db.save('user', name='李四', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
       assert db.get('select count(1) from user') == 2, 'count is 2'

       db.execute('update user set name=? where id=?', '王五', id2)
       assert db.get('select name from user where id=?', id2) == '王五', 'execute'

       db.execute('update user set name=:name where id=:id', name='赵六', id=id2)
       assert db.select_one('select id, name from user where id=:id', id=id2)[0] == id2, 'execute'

       db.execute('update user set name=:name where id=:id', name='赵六', id=id2)
       assert db.query_one('select name from user where id=:id', id=id2)['name'] == '赵六', 'execute'

       args = [
           ('张三', 55, '1968=-10-08', 0, 1.0, 20.5, 854.56),
           ('张三', 55, '1968=-10-08', 0, 1.0, 20.5, 854.56)
       ]
       db.batch_execute('insert into user(name, age, birth_date, sex, grade, point, money) values(?,?,?,?,?,?,?)', args)
       users = db.select('select id, del_flag from user')
       assert len(users) == 4, 'batch_execute'
       users = db.query('select id, del_flag from user')
       assert len(users) == 4, 'batch_execute'

       users = db.select('select id, del_flag from user where id=?', id2)
       assert len(users) == 1, 'select'
       users = db.query('select id, del_flag from user where id=?', id2)
       assert len(users) == 1, 'select'

       users = db.select('select id, del_flag from user where id=:id', id=id2)
       assert len(users) == 1, 'select'
       users = db.query('select id, del_flag from user where id=:id', id=id2)
       assert len(users) == 1, 'select'

       db.execute('delete from user where id=? limit 1', id2)
       assert db.get('select count(1) from user') == 3, 'execute delete'

Transaction
'''''''''''

::

   @db.with_transaction
   def test_transaction():
       db.insert('user', name='张三', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
       db.insert('user', name='李四', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)


   def test_transaction2():
       with db.transaction():
           db.insert('user', name='张三', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)
           db.insert('user', name='李四', age=55, birth_date='1968=-10-08', sex=0, grade=1.0, point=20.5, money=854.56)

Note: the functions return type
'''''''''''''''''''''''''''''''

::

   get: Return only one object, like count
   query_one: Return one row with dict
   select_one: Return one row with tuple
   find_by_id: Return one row with class instance object
   query: Return list of dict
   select: Return list of tuple
   find: Return list of class instance object
