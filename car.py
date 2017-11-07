# Initialize car based on RDW data


class Car:
    def __init__(self, **kwargs):
        if kwargs is not None:
            # not the prettiest of solutions, but at the current stage of abstraction not a lot of decisions have been made
            for key, value in kwargs.items():
                setattr(self, key, value)

    def parking_allowed(self):
        pass

    # TODO: Check if the car release is after 2001 AND uses a Diesel engine
    # dedicated API response field for this

    def get_number_plate(self):
        return self.number_plate

    def get_file_location(self):
        return self.file_location

    # Should be unavoided, but unavoidable
    def get_undefined_value(self, key):
        return getattr(self, key)