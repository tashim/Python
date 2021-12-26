from random import randint


class Wheel:

    def __init__(self, radius, punctured=False, air=None):

        # default value for air random between 85-95
        if air is None:
            self.air = randint(85, 95)
        # make sure air is integer
        else:
            self.air = int(air)

        # make sure air is between 0 -100
        if self.air > 100:
            self.air = 100
            # raise ValueError("air must be between 0 and 100")

        elif self.air < 0:
            self.air = 0

        self.punctured = bool(punctured)

        self.radius = int(radius)

        # make sure radius > 0:
        if self.radius < 1:
            self.radius = 1

    # printing for the user (the programmer)
    def __repr__(self):
        return "Wheel(radius={}, punctured={}, air={})".format(
            self.radius, self.punctured, self.air)

    # printing for the end-user
    def __str__(self):
        return "a {}wheel with {} radius & {}% air".format(
            "punctured " if self.punctured else "",
            self.radius,
            self.air
        )

    def inflate(self, air_to_add):
        self.air += air_to_add
        if self.air > 100:
            self.air = 100

