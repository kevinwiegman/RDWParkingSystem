import re


class NumberPlate():
    # UP TO DATE AS OF 11/6/2017, no container present so use at your own discretion
    def __init__(self, number_plate, validity_check=False):
        self.__number_plate = number_plate
        self.__valid_number_plate = None
        self.number_plate_regex()
        if validity_check:
            self.validate_number_plate()

    def number_plate_regex(self):
        self.REGEX = {
            1: "^[a-zA-Z]{2}[\d]{2}[\d]{2}$",  # XX-99-99
            2: "^[\d]{2}[\d]{2}[a-zA-Z]{2}$",  # 99-99-XX
            3: "^[\d]{2}[a-zA-Z]{2}[\d]{2}$",  # 99-XX-99
            4: "^[a-zA-Z]{2}[\d]{2}[a-zA-Z]{2}$",  # XX-99-XX
            5: "^[a-zA-Z]{2}[a-zA-Z]{2}[\d]{2}$",  # XX-XX-99
            6: "^[\d]{2}[a-zA-Z]{2}[a-zA-Z]{2}$",  # 99-XX-XX
            7: "^[\d]{2}[a-zA-Z]{3}[\d]{1}$",  # 99-XXX-9
            8: "^[\d]{1}[a-zA-Z]{3}[\d]{2}$",  # 9-XXX-99
            9: "^[a-zA-Z]{2}[\d]{3}[a-zA-Z]{1}$",  # XX-999-X
            10: "^[a-zA-Z]{1}[\d]{3}[a-zA-Z]{2}$",  # X-999-XX
            11: "^[a-zA-Z]{3}[\d]{2}[a-zA-Z]{1}$",  # XXX-99-X
            12: "^[a-zA-Z]{1}[\d]{2}[a-zA-Z]{3}$",  # X-99-XXX
            13: "^[\d]{1}[a-zA-Z]{2}[\d]{3}$",  # 9-XX-999
            14: "^[\d]{3}[a-zA-Z]{2}[\d]{1}$",  # 999-XX-9
            "CD": "^CD[ABFJNST][0-9]{1,3}$"  # CDB1 or CDJ45
        }

        self.FORMAT = {
            1: "%s%s-%s%s-%s%s",  # XX-99-99
            2: "%s%s-%s%s-%s%s",  # 99-99-XX
            3: "%s%s-%s%s-%s%s",  # 99-XX-99
            4: "%s%s-%s%s-%s%s",  # XX-99-XX
            5: "%s%s-%s%s-%s%s",  # XX-XX-99
            6: "%s%s-%s%s-%s%s",  # 99-XX-XX
            7: "%s%s-%s%s%s-%s",  # 99-XXX-9
            8: "%s-%s%s%s-%s%s",  # 9-XXX-99
            9: "%s%s-%s%s%s-%s",  # XX-999-X
            10: "%s-%s%s%s-%s%s",  # X-999-XX
            11: "%s%s%s-%s%s-%s",  # XXX-99-X
            12: "%s-%s%s-%s%s%s",  # X-99-XXX
            13: "%s-%s%s-%s%s%s",  # 9-XX-999
            14: "%s%s%s-%s%s-%s",  # 999-XX-9
            "CD": None  # CDB1 or CDJ45
        }

    def validate_number_plate(self):
        if self.__valid_number_plate is None:
            self.regex_match()

        return True

    def regex_match(self):
        for k, v in self.REGEX.items():
            print(self.stripped)
            hit = re.match(v, self.stripped)
            if hit is not None:
                self.__valid_number_plate = True
                return True
        self.__valid_number_plate = False
        return False

    def stripped(self):
        """ Removes dashes from a number plate
        XX-XX-XX becomes XXXXXX
        """
        return self.__number_plate.replace('-', '').strip().upper()

    def get_number_plate(self):
        """ Return"""
        return self.__number_plate
