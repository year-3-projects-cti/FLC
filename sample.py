# Variable assignment
x = 10
y = 20
z = x + y

# If-Else
if x > y:
    print("x is greater")
else:
    print("y is greater")

# For Loop
numbers = [1, 2, 3, 4]
for num in numbers:
    print(f"Number: {num}")

# While Loop
while x > 0:
    print(f"x is {x}")
    x -= 1

# Function Definition
def greet(name, age):
    print(f"Hello, {name}. You are {age} years old.")
greet("Alice", 30)

# Class Definition
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"My name is {self.name} and I am {self.age} years old.")

p = Person("Bob", 25)
p.introduce()

# Try-Except-Finally
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
finally:
    print("Done with division.")

# Match-Case
day = "Monday"
match day:
    case "Monday":
        print("Start of the week!")
    case "Friday":
        print("Almost the weekend!")
    case _:
        print("Just another day.")

# User Input
name = input("What is your name?")
age = input("How old are you?")
print(f"Hello, {name}. You are {age} years old.")
