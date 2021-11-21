import random

from animal import Animal


class Rat(Animal):

    def __init__(self, pos):
        Animal.__init__(self, pos)
        self.Combat_Effectiveness = random.uniform(1, 2)
        self.type = "rat"

    def detail(self):
        self.common_detail()

    def move(self, delta_x, delta_y):
        self.pos.move(2 * delta_x, 2 * delta_y)

    def des(self):
        x = self.pos.gotX()
        y = self.pos.gotY()

