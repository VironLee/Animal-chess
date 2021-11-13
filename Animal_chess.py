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

    temp_lands = copy.deepcopy(gameMap.landsArray)  # 深拷贝，防止随机过程对原来的数据产生影响
    random.shuffle(temp_lands)  # 将tempsArray随机打乱

    # 初始动物位置只能在land上
    num_animals = random.randint(1, gameMap.rows * gameMap.columns - len(gameMap.landsArray) - 1)
    animal_dict = {}

    #todo:须新增其他动物的自动生成逻辑
    for i in range(0, num_animals):
        pos = temp_lands[i]
        tiger = Tiger(pos)

        # 讲生成的老虎加入花名册
        animal_dict[tiger.id] = tiger

        # 在地图相应位置放置动物
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
        animal_dict = generate_random_animals(gameMap)
        return cls(gameMap, animal_dict)

    def game_situation(self):
        """
        打印当前时刻，游戏的状态
        Returns:

        """

        #存储整张地图的信息
        situation = ""

        #存储每一个grid的信息
        block_str = [["" for i in range(self.gameMap.columns)] for i in range(self.gameMap.rows)]

        #注意，这里采用的是逐列遍历，计算每一列的最大宽度用于对齐
        for j in range(self.gameMap.columns):
            width = 0
            for i in range(self.gameMap.rows):
                if self.gameMap.gridmatrix[i][j].OwnerId is None:
                    block_str[i][j] = self.gameMap.gridmatrix[i][j].property.name + " "
                else:
                    block_str[i][j] = self.gameMap.gridmatrix[i][j].property.name + " " + "\'" + self.animal_dict[
                        self.gameMap.gridmatrix[i][j].OwnerId].type + "\'"

                #更新这一列的最大宽度
                width = max(width, len(block_str[i][j]))

            #按照计算出来的最大宽度去对齐这一列的所有格子
            for k in range(self.gameMap.rows):
                block_str[k][j] = block_str[k][j].ljust(width) + " | "

        #所有格子逐行逐列拼接到situation中打印出来
        for i in range(self.gameMap.rows):
            for j in range(self.gameMap.columns):
                situation += block_str[i][j]
            situation += "\n"

        print(situation)
