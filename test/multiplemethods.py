#!/usr/bin/env python3

# in the context of nosetests `import yaz` is not available
from yaz import yaz

class Shape(yaz.Plugin):
    @yaz.task
    def circle(self):
        return "Circle"

    @yaz.task
    def square(self):
        return "Square"
# class FoodHelper(yaz.Plugin):
#     def output(self, message, shout):
#         if shout:
#             print(message.upper())
#         else:
#             print(message)

# class Food(yaz.Plugin):
#     def __init__(self, helper: FoodHelper):
#         self.helper = helper

#     @yaz.task
#     def breakfast(self, message="Breakfast is ready", shout:bool=False):
#         self.helper.output(message, shout)

#     @yaz.task
#     def lunch(self, message="Time for lunch", shout:bool=False):
#         self.helper.output(message, shout)

#     @yaz.task
#     def dinner(self, message="Dinner is served", shout:bool=False):
#         self.helper.output(message, shout)

if __name__ == "__main__":
    yaz.main()
