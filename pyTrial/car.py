class Car():
    def __init__(self, make, model, year):
        """Initialize"""
        self.make = make
        self.model = model
        self.year = year
        self.odometer_reading = 0

    def get_descriptive_name(self):
        """Return the descriptive information"""
        long_name = str(self.year) + ' ' + self.make + ' ' + self.model
        return long_name.title()

    def read_odometer(self):
        """Print the odometer information"""
        print("This car has " + str(self.odometer_reading) + " miles on it.")


my_new_car = Car('Audi', 'A6L', '2017')
print('My new car is ' + my_new_car.get_descriptive_name())
my_new_car.read_odometer()
