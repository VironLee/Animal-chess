import copy
import random

from Base import Map
from tiger import Tiger


def generate_random_animals(gameMap: Map) -> dict:
    """
    随机生成一系列动物，并注册到游戏内

    Args:
        gameMap: 地图

    Returns:动物花名册

    """

    temp_lands = copy.deepcopy(gameMap.landsArray)#深拷贝，防止随机过程对原来的数据产生影响
    random.shuffle(temp_lands)# 将tempsArray随机打乱

    #初始动物位置只能在land上
    num_animals = random.randint(1, gameMap.rows * gameMap.columns - len(gameMap.landsArray) - 1)
    animal_dict = {}
    for i in range(0, num_animals):
        pos = temp_lands[i]
        tiger = Tiger(pos)

        #讲生成的老虎加入花名册
        animal_dict[tiger.id] = tiger

        #在地图相应位置放置动物
        gameMap.put_animal(pos, tiger.id)

    return animal_dict


class Animal_chess:
    """
    总的游戏类

    Attributes:
        gameMap:地图
        animal_dict:动物花名册
    """
    gameMap: Map
    animal_dict: dict

    def __init__(self, gameMap: Map, animal_dict: dict):
        """
        用指定的地图和花名册创建游戏

        Args:
            gameMap: 地图
            animal_dict: 动物花名册
        """
        self.gameMap = gameMap
        self.animal_dict = animal_dict
        # self.gameMap.detail()
        self.game_situation()

    @classmethod
    def create_random_game(cls):
        """
        随机开一把游戏
        Returns:

        """
        gameMap = Map.generate_default_map()
        animal_dict= generate_random_animals(gameMap)
        return cls(gameMap, animal_dict)

    def game_situation(self):
        """
        打印当前时刻，游戏的状态
        Returns:

        """
        situation = ""
        for i in range(self.gameMap.rows):
            for j in range(self.gameMap.columns):
                if self.gameMap.gridmatrix[i][j].OwnerId is None:
                    #str.ljust(width) :左边对齐字符，对齐后的总长度是width
                    situation += (self.gameMap.gridmatrix[i][j].property.name.ljust(14) + " | ")
                else:
                    situation += (self.gameMap.gridmatrix[i][j].property.name + " " + "\'" + self.animal_dict[
                        self.gameMap.gridmatrix[i][j].OwnerId].type + "\'").ljust(14) + " | "
            situation += "\n"

        print(situation)

