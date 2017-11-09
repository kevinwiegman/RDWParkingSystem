# standard library imports
from inspect import currentframe, getframeinfo

# related third party imports
import pymysql

# local application/library specific imports
import config
import PSdebug

from car import Car
from validation import NumberPlate
from user import User


# TODO: User addition fields
# TODO: Optimization: variables for query's formatting in the object itself like the user example
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
                print(cursor.execute(sql, query_var))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        except:
            print(PSdebug.get_linenumber() + " CAR IMPORT ERROR")

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
            # TODO: Nice Error dump
            print(PSdebug.get_linenumber())

    def set_car_paid_by_number_plate(self, number_plate):
        try:
            with self.connection.cursor() as cursor:
                sql = "select paid from Log where id = (select max(id) from Log where `Kenteken` = %s)"
                cursor.execute(sql, (number_plate))
                state = cursor.fetchone()['paid']
                if state == 0:
                    paid = False
                else:
                    paid = True
                return paid
        except:
            raise Exception('Error during trying to find carr')

    def get_unreleased_car_record_by_number_plate(self, number_plate):

        if '-' in number_plate:
            number_plate = NumberPlate(number_plate).stripped()
        with self.connection.cursor() as cursor:
            sql = "select * from `Log` where `Kenteken` = %s and endTime = '1111-11-11 11:11:11'"
            # We only need to end time to calculate the duration of time
            print(cursor.execute(sql, (number_plate)))

            # Expected return dict looks like:
            # {'id': 3, 'Kenteken': '31-HP-HZ', 'startTime': datetime.datetime(2017, 6, 12, 10, 0), 'endTime': datetime.datetime(1111, 11, 11, 11, 11, 11), 'filename': 'c:/py/img/4'}
            return cursor.fetchone()
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
        with self.connection.cursor() as cursor:
            # Only want the amount of MINUTES, business rules need not be applied in query's
            sql = "SELECT timestampdiff(MINUTE, startTime, endTime) AS MINUTE FROM `Log`  where id = (SELECT MAX(ID) FROM `Log` WHERE `Kenteken` = %s)"
            print(dir(car))
            print(cursor.execute(sql, (car.get_number_plate())))
            timeDifference = cursor.fetchone()

            # Returns the amount of minutes in a whole number i.e 60
            return timeDifference['MINUTE']

        print(PSdebug.get_linenumber())

    def get_car_by_number_plate(self, number_plate):
        number_plate = NumberPlate(number_plate)
        try:
            with self.connection.cursor() as cursor:
                # Acquiring all car data
                sql = "SELECT * FROM `Log` WHERE `Kenteken` = %s"
                cursor.execute(sql, (number_plate.stripped()))
                car_data = cursor.fetchone()
                return Car(**car_data)
        except:
                print(PSdebug.get_linenumber())

    def insert_new_user_car_connection(self, number_plate, user_id):
        """Inserting a new record in the connecting table between cars and users"""
        # Acquiring the ID to connect both records
        record_id_car = self.get_unreleased_car_record_by_number_plate(number_plate)['id']
        query_var = (record_id_car, user_id)
        print(query_var)
        try:
            with self.connection.cursor() as cursor:
                # insert query
                sql = "INSERT INTO `ParkingLogin`(`idParking`, `idLogin`) VALUES(%s, %s);"
                cursor.execute(sql, query_var)
                # Commit's aren't handled automatic
                self.connection.commit()
        except:
            print(PSdebug.get_linenumber() + 'INSERT CONNECTION ERROR')

    def insert_new_user(self, user):
        """
        Two Query's -> Adding a new record to the user table and a new connection to a number plate
        Will be done using a transaction to be error correcting
        """
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `ParkingSystem`.`Login` (`name`, `email`, `phonenumber`, `streetname`, `postalcode`, `number`, `city`, `country`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            query_var = (user.get_invoice_data())
            cursor.execute(sql, query_var)
            self.insert_id = self.connection.insert_id()
            self.connection.commit()
            self.insert_new_user_car_connection(user.get_number_plate(), self.insert_id)
            # Commit's is done elsewhere hence absence

    def check_if_user_details_known_by_number_plate(self, number_plate):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `Login` where id = (SELECT idParking FROM `ParkingLogin` where idLogin = (SELECT MAX(ID) FROM `Log` WHERE `Kenteken` = %s AND paid = 1))"
                number_plate = NumberPlate(number_plate)
                cursor.execute(sql, (number_plate.stripped()))
                usr = cursor.fetchone()
                usr['kenteken'] = number_plate
                return User(**cursor.fetchone())
        except:
            print(PSdebug.get_linenumber() + 'USER KNOWN DATA ERROR')
