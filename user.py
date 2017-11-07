from db import Database

class User:

    def __init__(self, **kwargs):
        if kwargs is not None:
            for k, v in kwargs:
                setattr(self, k, v)

    def store_user(self):
        db = Database()
        db.insert_new_user(self)

    def get_invoice_data(self):
