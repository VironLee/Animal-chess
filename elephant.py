# mission: You need to complete methods below or even more
#         to simulate an elephant in this animal chess.The elephant
#          hunt any kind of animals except for rats
import random

from animal import Animal


class Elephant(Animal):
    def __init__(self, pos):
        Animal.__init__(self, pos)
        self.Combat_Effectiveness = random.uniform(1, 2)
        self.type = "elephant"

    def detail(self):
        self.common_detail()

    def move(self, delta_x, delta_y):
        self.pos.move(delta_x, delta_y)
