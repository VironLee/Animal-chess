import copy
import random
import uuid

from Base import GridProperty, Map, position
from animal import Animal
from elephant import Elephant
from rat import Rat
from tiger import Tiger


def check_range(game_map: Map, des: position) -> bool:
    des_x = des.x
    des_y = des.y
    row = game_map.rows
    column = game_map.columns

    if des_x >= column or des_y >= row:
        return False

    elif des_x < 0 or des_y < 0:
        return False

    else:
        return True


def check_valid(obj_id: uuid, delta_x: int, delta_y: int) -> int:
    obj: Animal
    obj = Animal_chess.animal_dict.get(obj_id)

    # 计算终点坐标
    des_x = obj.pos.x + delta_x
    des_y = obj.pos.y + delta_y

    # 通过终点坐标找到地块
    des = Animal_chess.gameMap.gridmatrix[des_y][des_x]

    # 查询地块属性
    if des.property == GridProperty.land:
        return 0

    if des.property == GridProperty.river:
        return 1

    if des.property == GridProperty.trap:
        return 2

    if des.property == GridProperty.target:
        pass


def check_owner(obj_id: uuid, delta_x: int, delta_y: int) -> bool:
    obj: Animal
    rival: Animal

    obj = Animal_chess.animal_dict.get(obj_id)
    des_x = obj.pos.x + delta_x
    des_y = obj.pos.y + delta_y
    des = Animal_chess.gameMap.gridmatrix[des_y][des_x]

    # 如果有主，找到占领者信息
    if des.OwnerId:
        return False

    else:
        return True


def rat_fight(obj_id: uuid, rival_id: uuid) -> bool:
    rival: Animal
    obj: Animal

    obj = Animal_chess.animal_dict.get(obj_id)
    rival = Animal_chess.animal_dict.get(rival_id)

    if rival.type == "tiger":
        return False

    if rival.type == "elephant":
        return True

    if rival.type == "rat":
        if obj.Combat_Effectiveness > rival.Combat_Effectiveness:
            return True

        if obj.Combat_Effectiveness < rival.Combat_Effectiveness:
            return False

        # 战力相同一起卒，更新地块信息
        # TODO：这里可以引入随机数去决定战斗结果
        if obj.Combat_Effectiveness == rival.Combat_Effectiveness:
            pass


def tiger_fight(obj_id: uuid, rival_id: uuid) -> bool:
    rival: Animal
    obj: Animal

    obj = Animal_chess.animal_dict.get(obj_id)
    rival = Animal_chess.animal_dict.get(rival_id)

    if rival.type == "elephant":
        return False

    if rival.type == "rat":
        return True

    if rival.type == "tiger":
        if obj.Combat_Effectiveness > rival.Combat_Effectiveness:
            return True

        if obj.Combat_Effectiveness < rival.Combat_Effectiveness:
            return False

        # 战力相同一起卒，更新地块信息
        # TODO：这里可以引入随机数去决定战斗结果
        if obj.Combat_Effectiveness == rival.Combat_Effectiveness:
            pass


def elephant_fight(obj_id: uuid, rival_id: uuid) -> bool:
    rival: Animal
    obj: Animal

    obj = Animal_chess.animal_dict.get(obj_id)
    rival = Animal_chess.animal_dict.get(rival_id)

    if rival.type == "rat":
        return False

    if rival.type == "tiger":
        return True

    if rival.type == "elephant":
        if obj.Combat_Effectiveness > rival.Combat_Effectiveness:
            return True

        if obj.Combat_Effectiveness < rival.Combat_Effectiveness:
            return False

        # 战力相同一起卒，更新地块信息
        # TODO：这里可以引入随机数去决定战斗结果
        if obj.Combat_Effectiveness == rival.Combat_Effectiveness:
            pass


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

    def animal_move(self, obj_id: uuid, delta_x: int, delta_y: int):
        obj: Animal
        rival: Animal

        # 通过id找到目标动物
        obj = self.animal_dict.get(obj_id)

        # 对动物坐标进行运算找到目标地块
        des_x = obj.pos.x + delta_x
        des_y = obj.pos.y + delta_y
        des = self.gameMap.gridmatrix[des_y][des_x]

        # 首先查看范围测试结果
        range_result = check_range(self.gameMap, position(des_x, des_y))

        if range_result:

            # 结果为真，则进行合法性测试
            valid_result = check_valid(obj_id, delta_x, delta_y)

            if valid_result == 0:

                # 结果为真，继续进行所有者测试
                ### 此时可以删除旧地信息
                owner_result = check_owner(obj_id, des_x, des_y)
                self.gameMap.gridmatrix[obj.pos.y][obj.pos.x].OwnerId = None

                if owner_result:

                    # 结果为真，说明此地无主，修改新旧两地信息
                    self.gameMap.gridmatrix[des_y][des_x].OwnerId = obj_id

                # 结果为假，通过id找到占领者
                else:
                    rival_id = des.OwnerId
                    rival = self.animal_dict.get(rival_id)

                    # 结果为假，则按动物类型进行打架测试
                    if obj.type == "rat":
                        fight_result = rat_fight(obj_id, rival_id)

                        # 赢了，修改数据，让它动起来，并修改对手状态为死
                        if fight_result:
                            self.gameMap.gridmatrix[des_y][des_x].OwnerId = obj_id
                            rival.wasHunted()

                        else:
                            obj.wasHunted()

                    if obj.type == "tiger":
                        fight_result = tiger_fight(obj_id, rival_id)

                        if fight_result:
                            self.gameMap.gridmatrix[des_y][des_x].OwnerId = obj_id
                            rival.wasHunted()

                        else:
                            obj.wasHunted()

                    if obj.type == "elephant":
                        fight_result = elephant_fight(obj_id, rival_id)

                        if fight_result:
                            self.gameMap.gridmatrix[des_y][des_x].OwnerId = obj_id
                            rival.wasHunted()

                        else:
                            obj.wasHunted()
            # 洞化
            elif valid_result == 2:
                self.gameMap.gridmatrix[obj.pos.y][obj.pos.x].OwnerId = None
                obj.getTrapped()

            # 游戏结束
            elif valid_result == 3:
                self.gameMap.gridmatrix[obj.pos.y][obj.pos.x].OwnerId = None
                Animal_chess.end_the_game()

    # TBD
    def end_the_game(self):
        pass

        # TODO：其他动物类的判定方法(封装）
