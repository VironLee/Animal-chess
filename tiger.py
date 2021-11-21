# mission: You need to complete methods below or even more
#         to simulate a tiger in this animal chess.The rat can jump over the river
#         and hunt any kind of animals except for elephants
import random

from animal import Animal


class Tiger(Animal):
    """
    老虎
    """

    def __init__(self, pos):
        Animal.__init__(self, pos)
        self.Combat_Effectiveness = random.uniform(1, 2)  # 老虎的战斗值在[1,2)之间
        self.type = "tiger"

    def detail(self):
        """
        打印该老虎的各项属性
        Returns:

        """
        self.common_detail()

    def move(self, delta_x: int, delta_y: int):
        self.pos.move(delta_x, delta_y)

    def des(self):
        x = self.pos.gotX()
        y = self.pos.gotY()
    
    # def move(self,des_x:int,des_y:int):
    #
    # def prey(self,animal)->bool:
