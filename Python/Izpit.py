class Car:
    def __init__(self, car_brand, car_model, car_price, car_color, manifacture_year):
        self.car_brand = car_brand
        self.car_model = car_model
        self.car_price = car_price
        self.car_color = car_color
        self.manifacture_year = manifacture_year

    def display_info(self):
        return f"({self.car_brand}, {self.car_model}, {self.car_price}, {self.car_color}, {self.manifacture_year})"

cars = [
    Car("BMW", "M5", 180000, "Blue", 2018),
    Car("BMW", "M8", 230000, "Black", 2019),
    Car("Ford", "Mustang", 80000, "Red", 2020),
    Car("Mercedes", "G-class", 280000, "Orange", 2023),
    Car("Opel", "Corsa", 13000, "Grey", 2022)
]

def sort_price(cars, car_price):
    cars.sort(key=lambda car: car.car_price, reverse=False)
    for car in cars:
        print(car.display_info())


def list_by_brand(cars, car_brand):
    n = input("Input a car brand:")
    for car in cars:
        if n == car.car_brand:
            print(car.display_info())

def search_color(cars, car_color):
    n = input("Input a car color:")
    for car in cars:
        if n == car.car_color:
            print(car.display_info())

def newest_car(cars):
    newest = max(cars, key=lambda car: car.manifacture_year)
    print(newest.display_info())

# Example usage
sort_price(cars)
list_by_brand(cars, "BMW")
search_color(cars, "Blue")
newest_car(cars)