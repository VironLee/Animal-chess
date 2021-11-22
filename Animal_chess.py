import copy
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

    # todo:须新增其他动物的自动生成逻辑
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

    def VitalCheck(self, id):
        obj: Animal
        rival: Animal
        des: Grid
        org: Grid
        self.id = id

        # 输入一个id，生成其对应的动物对象
        obj = self.animal_dict.get(self.id)
        
        # 生成动物对象所在地的地块对象
        org_x = obj.pos.gotX()
        org_y = obj.pos.gotY()
        org = Map.gridmatrix[org_x][org_y]

        # 生成目的地的地块对象
        obj.pos.move()
        des_x = obj.pos.gotX()
        des_y = obj.pos.gotY()
        des = Map.gridmatrix[des_x][des_y]

        # 老鼠类的判定方法
        if obj.type == "rat":

            # 目标点属性不为0，invalid的情况
            if des.property:
                if des.property == GridProperty.trap:
                    obj.getTrapped()

                    ### 下边这行用哪种表达方式可行？Answer:按照No.150行的语句来看，这两种写法是等价的
                    Map.gridmatrix[des_x][des_y].OwnerId = None
                    # org.OwnerId = None

                # 掉河里的状态没想好，暂定返回空值
                if des.property == GridProperty.river:
                    return None
            
            # 目标点属性为0，valid的情况，先清除原有信息
            else:
                org.OwnerId = None

                # 恰好移动到目标点，结束游戏
                #TODO：Target的value好像是3，不是0，是进不了这个else分支的
                if des.property == GridProperty.target: #TODO:即使到了Target也要先更新信息，再宣告游戏结束;完成Endthegame()的实现
                    Animal_chess.Endthegame()
                    
                # 移动到空地，更新地块占领信息
                if des.OwnerId == None:
                    des.isOccupiedBy(obj.id)

                # 不为空地，通过占有者信息判断状态
                if des.OwnerId:

                    # 生成占有地块的动物对象
                    rival = self.animal_dict.get(des.OwnerId)

                    if rival.type == "tiger":
                        obj.wasHunted()
                        
                    if rival.type == "elephant":
                        rival.wasHunted()
                        des.isOccupiedBy(obj.id)
                    
                    # 同类打架看战力，战力小的淘汰
                    if rival.type == "rat":
                        if obj.Combat_Effectiveness > rival.Combat_Effectiveness:
                            rival.wasHunted()
                            des.isOccupiedBy(obj.id)

                        if obj.Combat_Effectiveness < rival.Combat_Effectiveness:
                            obj.wasHunted()
                        
                        # 战力相同一起卒，更新地块信息
                        # TODO：这里可以引入随机数去决定战斗结果
                        if obj.Combat_Effectiveness == rival.Combat_Effectiveness:
                            obj.wasHunted()
                            rival.wasHunted()
                            des.OwnerId = None

        #TODO：其他动物类的判定方法(封装）