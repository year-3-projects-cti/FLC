x = 100
y = 20

if x > y:
    print(f"x is greater than y: {x} > {y}")
    if x > 5:
        print(f'x is mare amre')
        items = [1, 2, 3]
        for item in items:
            print(f"Item: {item}")
        xx = 0
        while xx < 5:
            print(f"x is {xx}")
            xx += 1


else:
    print(f"y is greater or equal to x: {y} >= {x}")

def greet(name):
    print(f"Hello, {name}")

if x > 5 and y < 10:
    print("Condition met")
my_dict = {"name": "Alice", "age": 30}

try:
    x = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
finally:
    print("Execution completed.")

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")
