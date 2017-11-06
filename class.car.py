# Initialize car based on RDW data


class Car:


    def __init__(self, **kwargs):
        if kwargs is not None:
            # not the prettiest of solutions, but at the current stage of abstraction not a lot of decisions have been made
            for key, value in kwargs.items():
                setattr(self, key, value)

    def parking_allowed(self):
        # TODO: Check if the car release is after 2001 AND uses a Diesel engine
        # dedicated API response field for this


