import db


class User:
    """Class used for routing user data, stores users in database and can return the data required for an invoice"""

    def __init__(self, **kwargs):
        if kwargs is not None:
            # TODO: should be replaced with set_vals function
            for k, v in kwargs.items():
                setattr(self, k, v)

    def invoice_data(self):
        return ['name', 'email', 'phonenumber', 'streetname', 'postalcode', 'number', 'city', 'country']

    def store_user(self):
        dataModel = db.Database()
        print(dataModel.insert_new_user(self))

    # Used to return only the relevant data for the invoice placed in the database
    def get_invoice_data(self):
        # Invoice data needs to be a tuple for the PyMySQL package
        invoice_data = ()
        # TODO: Optimize function
        for x in self.invoice_data():
            invoice_data = invoice_data + (getattr(self, x),)

        # Is a single tuple filled with only the data that has dedicated fields in the database
        return invoice_data

    def get_number_plate(self):
        return self.number_plate

    # Used for anonymous setters, should be replaced for 1.0
    def set_vals(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)
