import pymysql
import config
from inspect import currentframe, getframeinfo
import PSdebug

class Database(object):
    def __init__(self):
        self.frame = getframeinfo(currentframe())
        self.establish_connection()
        self.insert_record()

        # Check what the expected operation is i.e
        # 1. Gather data
        # 2. Place data
        # 3. Check data

    def establish_connection(self):
        try:
            self.connection = pymysql.connect(host=config.db['host'],
                                              user=config.db['user'],
                                              password=config.db['password'],
                                              db=config.db['db'],
                                              charset=config.db['charset'],
                                              cursorclass=pymysql.cursors.DictCursor)
        except:
            print('Error code DB.ES ' . PSdebug.get_linenumber())

    def insert_record(self):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        except:
            print(PSdebug.get_linenumber())


db = Database()
