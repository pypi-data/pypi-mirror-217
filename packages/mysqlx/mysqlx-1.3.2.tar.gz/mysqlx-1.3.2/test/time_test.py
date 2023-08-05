import unittest

sql = "INSERT INTO `user` (`name`,`age`,`birth_date`,`sex`,`grade`,`point`,`money`) VALUES (?,?,?,?,?,?,?)"


class MyTestCase(unittest.TestCase):
    def test_something(self):
        for _ in range(1000):
            sql.replace('?', '%s')
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
