#mission: You need to complete method of rat below or even more
#         to simulate a rat in this animal chess.The rat can swim (move in the water)
#         and hunt nobody but elephants.
import random

from animal import Animal


class Rat(Animal):
    def __init__(self, pos):
        Animal.__init__(self, pos)
        self.Combat_Effectiveness = random.uniform(1, 2)
        self.type = "rat"

    def detail(self):
        self.common_detail()

    def move(self, delta_x: int, delta_y: int):
        return super(Animal).move(delta_x, delta_y)
   # def __init__(self):
   #
   # def hunt(self):
   #
   # def move(self,delta_x,delta_y):

