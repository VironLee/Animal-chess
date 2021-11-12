#mission: You need to complete methods below or even more
#         to simulate a tiger in this animal chess.The rat can jump over the river
#         and hunt any kind of animals except for elephants
import random

from animal import Animal


class Tiger(Animal):

    def __init__(self,pos):
        Animal.__init__(self,pos)
        self.Combat_Effectiveness=random.uniform(1,2)

    def detail(self):
        print("Type:Tiger")
        self.common_detail()
    # def move(self,des_x:int,des_y:int):
    #
    # def prey(self,animal)->bool:
