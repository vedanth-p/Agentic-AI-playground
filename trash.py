from abc import ABC, abstractmethod

# User-defined exception
class EngineError(Exception):
    """Custom exception for engine-related errors."""
    pass


# Abstract class
class Vehicle(ABC):
    @abstractmethod
    def start_engine(self):
        """Every vehicle must implement this method."""
        pass
    


# Concrete class Car
class Car(Vehicle):
    def start_engine(self):
        print("Car engine started.")
    def print_sta(self):
        print("Dont be a bitch!")


# Concrete class Bike
class Bike(Vehicle):
    def __init__(self, has_fuel=True):
        self.has_fuel = has_fuel

    # def start_engine(self):
    #     if not self.has_fuel:
    #         raise EngineError("Bike cannot start: No fuel!")
    #     print("Bike engine started.")
        
    def pp(self):
        print("Small pp :(")


# Usage
try:
    my_car = Car()
    my_car.start_engine()   # ✅ Works fine
    my_car.print_sta()

    my_bike = Bike(has_fuel=False)
    my_bike.start_engine()  # ❌ Will raise EngineError
    my_bike.pp()

except EngineError as e:
    print("Engine Error:", e)
