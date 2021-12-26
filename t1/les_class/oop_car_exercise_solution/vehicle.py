from wheel import Wheel
from copy import deepcopy

class Vehicle:
    def is_drivable(self):
        if len(self.wheels) != 4:
            return False

        r = self.wheels[-1].radius

        for w in self.wheels:
            if w.punctured or w.air <= 60 or w.radius != r:
                return False

        return True

    # Warning: we do not set wheels argument to [] by default
    # otherwise, each new Vehicle with deafult wheels will
    # have the same list!
    def __init__(self, wheels=None):
        if wheels is None:
            wheels = []
        else:
            if not isinstance(wheels, list):
                raise ValueError("wheels must be a list of Wheel objects.")

            for w in wheels:
                if not isinstance(w, Wheel):
                    raise ValueError("wheels must be a list of Wheel objects.")

        #deepcopy so we use a different list with different Wheel objects
        self.wheels = deepcopy(wheels)
        self.drivable = self.is_drivable()

    def add_wheel(self, w):
        if isinstance(w, Wheel):
            self.wheels.append(w)
        else:
            raise ValueError("w must be a Wheel")

        self.drivable = self.is_drivable()

    def del_wheel(self, index=-1):
        self.wheels.pop(index)
        # del self.wheels[index]
        self.drivable = self.is_drivable()

    def __repr__(self):
        r = "Vehicle(wheels=[\n"

        for w in self.wheels:
            r += w.__repr__() + ", \n"

        r += "]) # "
        r += "drivable" if self.is_drivable() else "not drivable"
        return r

    def drive(self, distance):
        if not self.is_drivable():
            print("vehicle is not drivable")

        drivable_distance = min(w.air for w in self.wheels) - 60

        actual_distance = min(drivable_distance, distance)

        print("vehicle drove {} distance".format(actual_distance))
        for w in self.wheels:
            w.air -= actual_distance

        self.drivable = self.is_drivable()


    def drive_naive(self, distance):
        if not self.is_drivable():
            print("vehicle is not drivable")

        amount_driven = 0
        while self.is_drivable() and amount_driven != distance:
            for w in self.wheels:
                w.air -=1

            amount_driven += 1

        self.drivable = self.is_drivable()

        print("vehicle drove {} distance".format(amount_driven), end="")
        if amount_driven < distance:
            print(" before stopping.")

























