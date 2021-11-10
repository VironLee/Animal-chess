import random
from enum import Enum


class Status(Enum):
    """
    描述存活的状态
    """
    alive = 1
    dead = 0


class position:
    '''
    定义位置
    '''
    x: int
    y: int

    def __init__(self, x, y):
        """
        位置构造函数

        :param x: x坐标值
        :param y: y坐标值
        """
        self.x
        self.y

    def move(self, delta_x: int, delta_y: int):
        """
        移动位置

        :param delta_x: x方向移动量
        :param delta_y: y方向移动量
        :return:
        """
        self.x = self.x + delta_x
        self.y = self.y + delta_y


class River:
    def __init__(self, upper: int, left: int, height: int, width: int):
        """
        river的构造函数

        :param upper: river最上面的坐标
        :param left: river最左侧的坐标
        :param height: river的纵向宽度
        :param width: river的横向宽度
        """
        self.left = left
        self.upper = upper
        self.height = height
        self.width = width

    def flood(self, pos: position) -> bool:
        """
        判断输入的坐标是否在river范围内

        :param pos: 要判断的坐标
        :return: 在river范围内则返回True，反之返回False
        """
        if pos.x >= self.left and pos.x <= (self.left + self.width) and pos.x >= self.upper and pos.y <= (
                self.upper + self.height):
            return True
        else:
            return False


class Map:
    """
    地图
    """
    width: int
    length: int
    river: River
    target: position
    traps: list[position]

    def __init__(self, width: int, length: int, river: River, traps):
        """
        Map构造函数

        :param width: 地图纵向宽度
        :param length: 地图横向宽度
        :param river: 地图中的河流
        :param traps: 地图中的陷阱
        """
        self.width = width
        self.length = length
        self.rivers = river
        self.traps = traps

    @classmethod
    def generator_Default_map(cls):
        """
        生成默认地图，属于Map类的另一种构造函数
        默认地图尺寸是7x9，默认河流为一块3X3的区域，左上点在（3，4）

        :return:
        """
        default_width = 7
        default_length = 9
        river = River(3, 4, 3, 3)

        traps = []
        # 随机生成1~5个陷阱
        for i in range(random.randint(1, 5)):

            while True:
                trap = position(random.randint((0, default_width)), random.randint(0, default_length))
                # 保证陷阱不在河里面
                if river.flood(trap):
                    break

            traps.append(trap)

        return cls(7, 9, river, traps)
