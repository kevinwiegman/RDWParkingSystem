# standard library imports
from inspect import currentframe, getframeinfo

# related third party imports
import pymysql

# local application/library specific imports
import config
import PSdebug

from car import Car


# TODO: User addition fields
# TODO: Check if number plate already in system to avoid fraud

class Database:
    def __init__(self):
        self.frame = getframeinfo(currentframe())
        self.establish_connection()

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
            print('Error code DB.ES '.PSdebug.get_linenumber())

    # TODO: SQL injection prevention
    # TODO: Implement sanitazation earlier
    def insert_car(self, car):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `ParkingSystem`.`Log` (`Kenteken`, `endTime`, `filename`) VALUES (%s, '1111-11-11 11:11:11', %s);"
                query_var = (car.get_number_plate(), car.get_file_location())
                cursor.execute(sql, query_var)
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        except:
            print(PSdebug.get_linenumber())

    def get_unreleased_car_record_by_car(self, car):
        try:
            with self.connection.cursor() as cursor:
                sql = "select * from `Log` where `Kenteken` = %s and endTime = '1111-11-11 11:11:11'"
                # We only need to end time to calculate the duration of time
                cursor.execute(sql, (car.get_number_plate()))

                # Expected return dict looks like:
                # {'id': 3, 'Kenteken': '31-HP-HZ', 'startTime': datetime.datetime(2017, 6, 12, 10, 0), 'endTime': datetime.datetime(1111, 11, 11, 11, 11, 11), 'filename': 'c:/py/img/4'}
                return cursor.fetchone()
        except:
            print(PSdebug.get_linenumber())

    def set_unrealeased_car_to_released_by_car(self, car):
        try:
            with self.connection.cursor() as cursor:
                # TODO: REALLY NEED TO OPTIMIZE THIS, HIGH PRIORITY BACKLOG
                sql = "UPDATE `ParkingSystem`.`Log` SET `endTime` = CURRENT_TIMESTAMP WHERE ID= (SELECT MAX(ID) FROM (select * from `Log` )as x WHERE x.`Kenteken` = %s);"
                print(sql)
                cursor.execute(sql, (car.get_number_plate()))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        except:
            print(PSdebug.get_linenumber())

    # TODO: Create dynamic variables
    def get_released_car_duration_by_car(self, car):
        try:
            with self.connection.cursor() as cursor:
                # Only want the amount of MINUTES, business rules need not be applied in query's
                sql = "SELECT timestampdiff(MINUTE, startTime, endTime) AS MINUTE FROM `Log`PSdebug where id = (SELECT MAX(ID) FROM `Log` WHERE `Kenteken` = %s)"
                cursor.execute(sql, (car.get_number_plate()))
                timeDifference = cursor.fetchone()

                # Returns the amount of minutes in a whole number i.e 60
                return timeDifference['MINUTE']
        except:
            print(PSdebug.get_linenumber())

    def get_car_by_number_plate(self, number_plate):
        try:
            with self.connection.cursor() as cursor:
                # Acquiring all car data
                sql = "SELECT * FROM `Log` WHERE `Kenteken` = %s)"
                cursor.execute(sql, (number_plate))

                return Car(cursor.fetchone())
        except:
            print(PSdebug.get_linenumber())

    def insert_new_user_car_connection(self, number_plate, user_id):
        """Inserting a new record in the connecting table between cars and users"""

        # Acquiring the ID to connect both records
        record_id_car = self.get_unreleased_car_record_by_number_plate()
        query_var = (record_id_car, user_id)
        try:
            with self.connection.cursor() as cursor:
                # insert query
                sql = "INSERT INTO `ParkingLogin`(`idParking`, `idLogin`) VALUES(%s, %s);"
                cursor.execute(sql, query_var)
                # Commit's aren't handled automatic
                self.connection.commit()
        except:
            print(PSdebug.get_linenumber())

    def insert_new_user(self, user):
        """
        Two Query's -> Adding a new record to the user table and a new connection to a number plate
        Will be done using a transaction to be error correcting
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `ParkingSystem`.`Login` (`name`, `email`, `streetname`, `postalcode`, `number`, `city`, `country`) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                query_var = (user.get_invoice_data())
                cursor.execute(sql, query_var)
                self.insert_new_user_car_connection(user.get_number_plate(), cursor.lastrowid)
                # Commit's is done elsewhere hence absence
        except:
            print(PSdebug.get_linenumber())
