import copy
import random
import uuid

import animal
from Base import GridProperty, Map, position, AnimalStatus, BattleResult
from animal import Animal
from elephant import Elephant
from rat import Rat
from tiger import Tiger


def calc_battle_result(obj: animal, enemy: animal) -> AnimalStatus:
    # 计算可能的比较结果
    if obj.type == enemy.type:
        if obj.Combat_Effectiveness > enemy.Combat_Effectiveness:
            result = BattleResult.win
            return result
        else:
            result = BattleResult.loss  # 简化规则，主场优势，战斗值一样主场获胜
            return result

    if obj.type == "rat":
        if enemy.type == " tiger":
            result = BattleResult.loss
            return result
        elif enemy.type == "elephant":
            result = BattleResult.win
            return result

    elif obj.type == "tiger":
        if enemy.type == " elephant":
            result = BattleResult.loss
            return result
        elif enemy.type == "rat":
            result = BattleResult.win
            return result

    elif obj.type == "elephant":
        if enemy.type == "rat":
            result = BattleResult.loss
            return result
        elif enemy.type == "tiger":
            result = BattleResult.win
            return result


def generate_test_animals(gameMap: Map) -> dict:
    """
    随机生成一系列动物，并注册到游戏内,用于测试

    Args:
        gameMap: 地图

    Returns:动物花名册

    """

    temp_lands = copy.deepcopy(gameMap.landsArray)  # 深拷贝，防止随机过程对原来的数据产生影响
    random.shuffle(temp_lands)  # 将tempsArray随机打乱

    # 初始动物位置只能在land上
    animal_dict = {}

    a = 3  # 随机生成老虎数量
    for i in range(0, a):  # 确定老虎在字典中的位置
        pos = temp_lands[i]
        tiger = Tiger(pos)

        # 每执行一次循环，将生成的老虎加入花名册
        # id作为key,动物对象作为value
        animal_dict[tiger.id] = tiger

        # 在地图相应位置放置动物
        gameMap.put_animal(pos, tiger.id)

    b = 8  # 生成老鼠数量
    for j in range(a, a + b):  # 确定老鼠在字典中的位置
        pos = temp_lands[j]
        rat = Rat(pos)

        animal_dict[rat.id] = rat

        gameMap.put_animal(pos, rat.id)

    c = 4  # 生成大象数量

    for k in range(b, b + c):
        pos = temp_lands[k]
        elephant = Elephant(pos)

        animal_dict[elephant.id] = elephant

        gameMap.put_animal(pos, elephant.id)

    print(a, b, c)  # 打印三种动物数量
    return animal_dict


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

    @classmethod
    def create_test_game(cls):
        """
        测试服
        Returns:
        """
        gameMap = Map.generate_default_map()
        animal_dict = generate_test_animals(gameMap)
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

    def check_range(self, game_map: Map, des: position) -> bool:
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

    def check_valid(self, obj_id: uuid, delta_x: int, delta_y: int) -> int:
        obj: Animal
        obj = self.animal_dict.get(obj_id)

        # 计算终点坐标
        des_x = obj.pos.x + delta_x
        des_y = obj.pos.y + delta_y

        # 通过终点坐标找到地块
        des = self.gameMap.gridmatrix[des_y][des_x]

        # 查询地块属性
        if des.property == GridProperty.land:
            return 0

        if des.property == GridProperty.river:
            return 1

        if des.property == GridProperty.trap:
            return 2

        if des.property == GridProperty.target:
            return 3

    def check_owner(self, des_x: int, des_y: int) -> bool:
        des = self.gameMap.gridmatrix[des_y][des_x]

        # 如果有主，找到占领者信息
        if des.OwnerId:
            return False

        else:
            return True

    def rat_fight(self, obj_id: uuid, rival_id: uuid) -> bool:
        rival: Animal
        obj: Animal

        obj = self.animal_dict.get(obj_id)
        rival = self.animal_dict.get(rival_id)

        if rival.type == "tiger":
            return False

        if rival.type == "elephant":
            return True

        if rival.type == "rat":
            if obj.Combat_Effectiveness > rival.Combat_Effectiveness:
                return True

            else:
                return False

    def tiger_fight(self, obj_id: uuid, rival_id: uuid) -> bool:
        rival: Animal
        obj: Animal

        obj = self.animal_dict.get(obj_id)
        rival = self.animal_dict.get(rival_id)

        if rival.type == "elephant":
            return False

        if rival.type == "rat":
            return True

        if rival.type == "tiger":
            if obj.Combat_Effectiveness > rival.Combat_Effectiveness:
                return True

            else:
                return False

    def elephant_fight(self, obj_id: uuid, rival_id: uuid) -> bool:
        rival: Animal
        obj: Animal

        obj = self.animal_dict.get(obj_id)
        rival = self.animal_dict.get(rival_id)

        if rival.type == "rat":
            return False

        if rival.type == "tiger":
            return True

        if rival.type == "elephant":
            if obj.Combat_Effectiveness > rival.Combat_Effectiveness:
                return True

            else:
                return False

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
        range_result = self.check_range(self.gameMap, position(des_x, des_y))

        if range_result:

            # 结果为真，则进行合法性测试
            valid_result = self.check_valid(obj_id, delta_x, delta_y)

            if valid_result == 0:

                # 结果为真，继续进行所有者测试
                ### 此时可以删除旧地信息，并修改动物坐标
                owner_result = self.check_owner(des_x, des_y)
                self.gameMap.gridmatrix[obj.pos.y][obj.pos.x].OwnerId = None
                obj.pos = position(des_x, des_y)

                if owner_result:

                    # 结果为真，说明此地无主，修改新旧两地信息
                    self.gameMap.gridmatrix[des_y][des_x].OwnerId = obj_id

                # 结果为假，通过id找到占领者
                else:
                    rival_id = des.OwnerId
                    rival = self.animal_dict.get(rival_id)

                    # 结果为假，则按动物类型进行打架测试
                    if obj.type == "rat":
                        fight_result = self.rat_fight(obj_id, rival_id)

                        # 赢了，修改数据，让它动起来，并修改对手状态为死
                        if fight_result:
                            self.gameMap.gridmatrix[des_y][des_x].OwnerId = obj_id
                            rival.wasHunted()

                        else:
                            obj.wasHunted()

                    if obj.type == "tiger":
                        fight_result = self.tiger_fight(obj_id, rival_id)

                        if fight_result:
                            self.gameMap.gridmatrix[des_y][des_x].OwnerId = obj_id
                            rival.wasHunted()

                        else:
                            obj.wasHunted()

                    if obj.type == "elephant":
                        fight_result = self.elephant_fight(obj_id, rival_id)

                        if fight_result:
                            self.gameMap.gridmatrix[des_y][des_x].OwnerId = obj_id
                            rival.wasHunted()

                        else:
                            obj.wasHunted()
            # 洞化
            elif valid_result == 2:
                self.gameMap.gridmatrix[obj.pos.y][obj.pos.x].OwnerId = None
                obj.pos = position(des_x, des_y)
                obj.getTrapped()

            # 游戏结束
            elif valid_result == 3:
                self.gameMap.gridmatrix[obj.pos.y][obj.pos.x].OwnerId = None
                obj.pos = position(des_x, des_y)
                self.end_the_game()

    def find_specific_animal(self, animal_type: str) -> Animal:
        """
        找到一个指定种类的活的动物对象
        Args:
            animal_type: 指定动物种类

        Returns:

        """
        for id in self.animal_dict:
            if self.animal_dict[id].type == animal_type and self.animal_dict.get(id).status == AnimalStatus.alive:
                return self.animal_dict[id]

        print("can not find a specific animal!")

    def find_specific_grid(self, grid_type: str) -> position:
        """
        找到一个指定类型的地块的位置
        Args:
            gird_type: 地块类型（land or river or target or trap)

        Returns:

        """
        match grid_type:

            case "land":
                grid_array = copy.deepcopy(self.gameMap.landsArray)  # 深拷贝

            case "river":
                grid_array = copy.deepcopy(self.gameMap.riverArray)

            case "trap":
                grid_array = copy.deepcopy(self.gameMap.trapsArray)

            case "target":
                return self.gameMap.target

        if len(grid_array) <= 0:  # 地块数组数量小于等于0，异常情况
            print("can not find a specific grid pos")
            return None

        # 随机排列地块数组
        random.shuffle(grid_array)
        # 如果是land，则要排除有动物的地块
        if grid_type == "land":
            for p in grid_array:
                if self.gameMap.gridmatrix[p.y][p.x].OwnerId is None:
                    return p

        return grid_array[0]

    def move_test(self, animal_type: str, grid_type: str, test_index: int) -> bool:
        """
        测试：把某一种动物的一个对象，移动到某种地块上
        Args:
            animal_type: 动物种类
            grid_type: 地块种类

        Returns:

        """

        # 找到一个符合条件的动物对象
        anim = self.find_specific_animal(animal_type)
        if anim is None:
            return False
        # 找到一个符合条件的地块位置
        grid_pos = self.find_specific_grid(grid_type)
        if grid_pos is None:
            return False

        # 打印日志
        print("*****************MOVE Test " + str(test_index) + "************************")
        print("移动的动物对象是：")
        anim.common_detail()
        print("目标点属性：" + grid_type + ",坐标：" + str(grid_pos.x) + "," + str(grid_pos.y) + ")")

        # 记录原始数据
        orgin_x = anim.pos.x
        orgin_y = anim.pos.y

        # 计算delta_x,delta_y,并执行移动函数
        delta_x = grid_pos.x - anim.pos.x
        delta_y = grid_pos.y - anim.pos.y
        self.animal_move(anim.id, delta_x, delta_y)

        # 数据校验
        self.game_situation()  # 展示全局结果

        match grid_type:
            # 如果是洞，检查动物是否死掉，还有位置是否更新
            case "trap":
                if self.gameMap.gridmatrix[orgin_y][orgin_x].OwnerId != None:
                    print("Error:没有清除原位置上的ownerID!!!")
                    print("*****************************************************")
                    return False
                if anim.status != AnimalStatus.dead:
                    print("Error:洞化后居然还活着？牛逼!!! check trap逻辑")
                    print("*************************************************")
                    return False
                elif anim.pos.x != grid_pos.x or anim.pos.y != grid_pos.y:
                    print("Error:生要见人死要见尸，死在哪里了？check trap逻辑")
                    print("**************************************************")
                    return False
            # 如果是河，检查位置是否保持不动
            case "river":
                if anim.pos.x != orgin_x or anim.pos.y != orgin_y:
                    print("Error: destination在河里，动不得。请check river的逻辑")
                    print("*************************************************")
                    return False

            # 如果是土地 or target，只需要检查是否到达目的地
            case "land" | "target":
                if self.gameMap.gridmatrix[orgin_y][orgin_x].OwnerId != None:
                    print("Error:没有清除原位置上的ownerID!!!")
                    print("*****************************************************")
                    return False
                if anim.pos.x != grid_pos.x or anim.pos.y != grid_pos.y:
                    print("Error:没有走对位置，animal当前位置应是（" + str(grid_pos.x) + "," + str(grid_pos.y) + ",实际值是（" + str(
                        anim.pos.x) + "," + str(anim.pos.y) + "),请检查在land上move的逻辑")
                    print("*************************************************")
                    return False

        print("************************success***************************")
        return True

    def find_an_different_animal(self, obj_id: uuid, enemy_type: str) -> Animal:
        for id in self.animal_dict:
            if id != obj_id:
                if self.animal_dict[id].type == enemy_type and self.animal_dict.get(id).status == AnimalStatus.alive:
                    enemy = self.animal_dict[id]

                    return enemy

        print("can not find a specific animal!")

    def battle_test(self, obj_type: str, enemy_type: str, test_index: int) -> bool:

        # 找到一个符合条件的动物对象
        if obj_type != enemy_type:
            obj = self.find_specific_animal(obj_type)
            if obj is None:
                return False
            # 找到一个符合条件的动物对象
            enemy = self.find_specific_animal(enemy_type)

        if obj_type == enemy_type:
            obj = self.find_specific_animal(obj_type)
            enemy = self.find_an_different_animal(obj.id, enemy_type)
            if enemy is None:
                return False

        # 打印日志
        print("***********************Battle test " + str(test_index) + "**************************")
        print("The obj is :")
        obj.common_detail()
        print("The enemy is :")
        enemy.common_detail()

        # 记录原始数据
        orgin_x = obj.pos.x
        orgin_y = obj.pos.y

        target_x = enemy.pos.x
        target_y = enemy.pos.y

        # 计算battle result
        result = calc_battle_result(obj, enemy)

        # 计算delta x,delta_x，执行move函数
        delta_x = target_x - orgin_x
        delta_y = target_y - orgin_y
        self.animal_move(obj.id, delta_x, delta_y)

        # 校验数据
        self.game_situation()  # 展示全局结果
        if self.gameMap.gridmatrix[orgin_y][orgin_x].OwnerId != None:
            print("Error:没有清除原位置上的ownerID!!!")
            print("*************************************************")
            return False

        match result:
            # 如果打得赢，验证终点的owner id，obj/enemy的状态，obj的坐标
            case BattleResult.win:
                if obj.status is not AnimalStatus.alive or enemy.status is not AnimalStatus.dead:
                    print("Error:obj打赢了，但却出现赢家死了，或，输家还活着？请检查！")
                    print("*************************************************")
                    return False
                elif self.gameMap.gridmatrix[target_y][target_x].OwnerId is not obj.id:
                    print("Error:打赢了！为什么地皮还不改名字？？")
                    print("*************************************************")
                    return False
                elif obj.pos.x != target_x or obj.pos.y != target_y:
                    print("Error:打赢了，但obj的位置未更新！")
                    print("*************************************************")
                    return False

            # 打输了，检查obj/enemy的状态，终点的ownerID,和obj的坐标
            case BattleResult.loss:
                if obj.status is not AnimalStatus.dead or enemy.status is not AnimalStatus.alive:
                    print("Error:obj打输了,但却出现赢家死了，或，输家还活着？请检查！")
                    print("*************************************************")
                    return False
                elif self.gameMap.gridmatrix[target_y][target_x].OwnerId is not enemy.id:
                    print("Error:打输了！为什么地皮改名字了？？")
                    print("*************************************************")
                    return False
                elif obj.pos.x != target_x or obj.pos.y != target_y:
                    print("Error:打输了，但obj的尸体位置未更新！")
                    print("*************************************************")
                    return False

        print("*************************success************************")
        return True

    # TBD
    def end_the_game(self):
        pass

