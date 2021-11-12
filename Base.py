import random
import uuid
from enum import Enum


class AnimalStatus(Enum):
    """
    描述存活的状态
    """
    alive = 1
    dead = 0


class GridProperty(Enum):
    """
    描述地块的属性
    """
    land = 0
    river = 1
    trap = 2
    target = 3


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
        self.x = x
        self.y = y

    def move(self, delta_x: int, delta_y: int):
        """
        移动位置

        :param delta_x: x方向移动量
        :param delta_y: y方向移动量
        :return:
        """
        self.x = self.x + delta_x
        self.y = self.y + delta_y

    def detail(self) -> str:
        return "(" + str(self.x) + "," + str(self.y) + ")"


class Grid:
    property: GridProperty
    OwnerId: uuid

    def __init__(self, property: GridProperty):
        self.property = property
        self.OwnerId = None

    @classmethod
    def create_default_grid(cls):
        return cls(GridProperty.land)

    def isOccupiedBy(self, animal_uuid: uuid):
        """
        地块被新的动物占领，更新OwnerId

        :param animal_uuid:新占有者的uuid
        :return:
        """
        self.OwnerId = animal_uuid

    def detail(self) -> str:
        return str(self.property.name) + " " + str(self.OwnerId) + "|"


class Map:
    """
    地图
    """
    rows: int
    columns: int
    gridmatrix: list[list[Grid]]
    num_of_traps: int

    def __init__(self, rows: int, columns: int, gridmatrix: list[list[Grid]]):
        """
        Map构造函数

        :param rows: 地图行数
        :param columns: 地图列数
        :param gridmatrix: 地块矩阵
        """
        self.rows = rows
        self.columns = columns
        self.gridmatrix = gridmatrix

        self.num_of_traps = 0
        for i in range(len(gridmatrix)):
            for j in range(len(gridmatrix[0])):
                if gridmatrix[i][j].property == GridProperty.trap:
                    self.num_of_traps += 1

    @classmethod
    def generate_default_map(cls):
        """
        生成默认地图，属于Map类的另一种构造函数
        默认地图尺寸是7x9，默认河流为一块3X3的区域，左上点在（2，3）(像素坐标系，从0开始计算)

        :return:
        """
        default_rows = 7
        default_cols = 9

        # 生成7x9的grid matrix
        grids = [[Grid.create_default_grid() for i in range(default_cols)] for i in range(default_rows)]

        # 设置river
        for i in range(2, 5):
            for j in range(3, 6):
                grids[i][j].property = GridProperty.river

        # 随机生成target position，且要保证它不在河里
        while True:
            target = position(random.randint(0, default_cols - 1), random.randint(0, default_rows - 1))
            if grids[target.y][target.x].property == GridProperty.land:
                grids[target.y][target.x].property = GridProperty.target
                break

        # 随机生成1~5个陷阱
        num_traps = random.randint(1, 5)
        for i in range(num_traps):
            while True:
                trap = position(random.randint(0, default_cols - 1), random.randint(0, default_rows - 1))
                # 保证陷阱不在河里面
                if grids[trap.y][trap.x].property == GridProperty.land:
                    grids[trap.y][trap.x].property = GridProperty.trap
                    break

        return cls(7, 9, grids)

    def detail(self):
        """
        打印Map信息
        """
        print("The map is " + str(self.rows) + "x" + str(self.columns))
        print("num of trap:" + str(self.num_of_traps))
        grid_info = ""
        for i in range(self.rows):
            for j in range(self.columns):
                grid_info += "(" + str(j) + "," + str(i) + ")" + self.gridmatrix[i][j].detail()
            grid_info += "\n"
        print(grid_info)
