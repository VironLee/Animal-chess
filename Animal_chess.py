import copy
from enum import Enum
import random

from Base import Grid, GridProperty, Map, position
from animal import Animal
from elephant import Elephant
from rat import Rat
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
    animal_dict = {}

    a = random.randint(1, len(temp_lands) - 2)  # 随机生成老虎数量
    for i in range(0, a):  # 确定老虎在字典中的位置
        pos = temp_lands[i]
        tiger = Tiger(pos)

        # 每执行一次循环，将生成的老虎加入花名册
        # id作为key,动物对象作为value
        animal_dict[tiger.id] = tiger

        # 在地图相应位置放置动物
        gameMap.put_animal(pos, tiger.id)

    b = random.randint(1, len(temp_lands) - len(animal_dict))  # 生成老鼠数量
    for j in range(a, a + b):  # 确定老鼠在字典中的位置
        pos = temp_lands[j]
        rat = Rat(pos)

        animal_dict[rat.id] = rat

        gameMap.put_animal(pos, rat.id)

    c = random.randint(1, len(temp_lands) - len(animal_dict))  # 生成大象数量

    for k in range(b, b + c):
        pos = temp_lands[k]
        elephant = Elephant(pos)

        animal_dict[elephant.id] = elephant

        gameMap.put_animal(pos, elephant.id)

    print(a, b, c)  # 打印三种动物数量
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

        # 存储整张地图的信息
        situation = ""

        # 存储每一个grid的信息
        block_str = [["" for i in range(self.gameMap.columns)] for i in range(self.gameMap.rows)]

        # 注意，这里采用的是逐列遍历，计算每一列的最大宽度用于对齐
        for j in range(self.gameMap.columns):
            width = 0
            for i in range(self.gameMap.rows):
                if self.gameMap.gridmatrix[i][j].OwnerId is None:
                    block_str[i][j] = self.gameMap.gridmatrix[i][j].property.name + " "
                else:
                    block_str[i][j] = self.gameMap.gridmatrix[i][j].property.name + " " + "\'" + self.animal_dict[
                        self.gameMap.gridmatrix[i][j].OwnerId].type + "\'"

                # 更新这一列的最大宽度
                width = max(width, len(block_str[i][j]))

            # 按照计算出来的最大宽度去对齐这一列的所有格子
            for k in range(self.gameMap.rows):
                block_str[k][j] = block_str[k][j].ljust(width) + " | "

        # 所有格子逐行逐列拼接到situation中打印出来
        for i in range(self.gameMap.rows):
            for j in range(self.gameMap.columns):
                situation += block_str[i][j]
            situation += "\n"

        print(situation)

    def check_range(self, map: Map, des: position) -> bool:
        des_x = des.x
        des_y = des.y
        row = map.rows
        column = map.columns

        if des_x >= column or des_y >= row:
            return False

        elif des_x < 0 or des_y < 0:
            return False

        else:
            return True
        
    def rat_check_valid(self, org: position, delta_x: int, delta_y: int) -> bool:
        rival: Animal

        # 计算终点坐标
        des_x = org.x + delta_x
        des_y = org.y + delta_y

        # 通过终点坐标找到地块
        des = Animal_chess.gameMap.gridmatrix[des_y][des_x]

        # 查询地块属性
        if des.property == GridProperty.target:
            return True

        elif des.property == GridProperty.land:
            if des.OwnerId:
                rival = self.animal_dict.get(des.OwnerId)
            
                if rival.type == "tiger":
                    return False
                
                if rival.type == "elephant":
                    return True

                if rival.type == "rat":
                    return True

            else:
                return True

        else:
            return False
        
    def rat_fight(self: Animal) -> Enum:
        rival: Animal
        win = 1
        lose = 0
        des = Animal_chess.gameMap.gridmatrix[7][7]
        rival = Animal_chess.animal_dict.get(des.OwnerId)
        
        if rival.type == "elephant":
            return win
            
        if rival.type == "rat":
            if self.Combat_Effectiveness > rival.Combat_Effectiveness:
                return win

            if self.Combat_Effectiveness < rival.Combat_Effectiveness:
                return lose
                        
            # 战力相同一起卒，更新地块信息
            # TODO：这里可以引入随机数去决定战斗结果
            if self.Combat_Effectiveness == rival.Combat_Effectiveness:
                return lose
        
    def rat_move(self):
        result = self.rat_check_valid(position(2, 4), 5, 3) and self.check_range(Map, position(7, 7))
        
        if result:
            Rat.move()

        else:
            Rat.stop()

    def find_an_object(self, id):
        obj: Animal
        self.id = id

        # 输入一个id，生成其对应的动物对象
        obj = Animal_chess.animal_dict.get(self.id)
        
        if obj.type == "rat":
            result = self.rat_move()

            if result:
                fight_result = self.rat_fight()

                if fight_result:
                    Animal_chess.gameMap.put_animal(position(7, 7), self.id)

                else:
                    obj.wasHunted()


        if obj.type == "tiger":
            self.tiger_move()

        if obj.type == "elephant":
            self.elephant_move()


        #TODO：其他动物类的判定方法(封装）