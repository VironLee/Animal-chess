import random
import uuid
from enum import Enum

from Global import animal_dict


class AnimalStatus(Enum):
    """
    描述存活的状态

    Attributes:
        alive:1
        dead:0
    """
    alive = 1
    dead = 0


class GridProperty(Enum):
    """
    Definitions of grid type

    Attributes:
        land: 0. Normal grid,all kinds of animals can stay here.
        river: 1.Only animals which able to swim can stay here.
        trap:2. Animal will die if step here.
        target:3. Winner!
    """
    land = 0
    river = 1
    trap = 2
    target = 3


class position:
    '''
    定义位置

    Attributes：
        x:位于第几列
        y:位于第几行
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
    """
    地块，地图的基本组成单元

    Attributes:
        property:类型
        OwnerId:占据这个地块的动物id
    """
    property: GridProperty
    OwnerId: uuid

    def __init__(self, property: GridProperty):
        """
        Grid构造函数

        Args:
            property: type of this grid
        """
        self.property = property
        self.OwnerId = None

    @classmethod
    def create_default_grid(cls):
        """
        构造默认Grid(land)
        Returns:

        """
        return cls(GridProperty.land)

    def isOccupiedBy(self, animal_uuid: uuid):
        """
        地块被新的动物占领，更新OwnerId

        :param animal_uuid:新占有者的uuid
        :return:
        """
        self.OwnerId = animal_uuid

    def detail(self) -> str:
        if self.OwnerId is None:
            return str(self.property.name) + " | "
        return str(self.property.name) + " " + animal_dict[self.OwnerId].type + " | "


class Map:
    """
    地图类

    Attributes:
        rows:行数，M
        coloumns:列数，N
        gridmatrix:grid矩阵，地图就是由MXN个grid组成的矩阵
        landsArray:储存土地位置的数组
        riverArray:储存河流位置的数组
        trapsArray:储存陷阱位置的数组
        target:目标点位置

    """
    rows: int
    columns: int
    gridmatrix: list[list[Grid]]
    landsArray: list[position]
    riverArray: list[position]
    trapsArray: list[position]

    target: position

    # num_of_traps: int

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

        self.landsArray = []
        self.riverArray = []
        self.trapsArray = []

        self.__summary_grids()

    @classmethod
    def generate_default_map(cls):
        """
        生成默认地图，属于Map类的另一种构造函数
        默认地图尺寸是7x9，默认河流为一块3X3的区域，左上点在（第2列，第3行）(像素坐标系，从0开始计算)

        :return:a default map
        """
        default_rows = 7
        default_cols = 9

        # 生成7x9的grid matrix，首先默认都是land
        grids = [[Grid.create_default_grid() for i in range(default_cols)] for i in range(default_rows)]

        # 设置river
        for i in range(3, 6):
            for j in range(2, 5):
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
                # 保证陷阱不在河里面，也不与target重合
                if grids[trap.y][trap.x].property == GridProperty.land:
                    grids[trap.y][trap.x].property = GridProperty.trap
                    break

        return cls(7, 9, grids)

    def put_animal(self, pos: position, animal_id: uuid):
        """
        在地图上放置动物，起始就是修改相应位置的grid的OwnerId

        :param pos:放置的位置
        :param animal_id:动物的id
        :return:
        """
        self.gridmatrix[pos.y][pos.x].OwnerId = animal_id

    def __summary_grids(self):
        """
        统计地图上个各种类型的grid，并把他们的位置储存在array中

        Returns:

        """
        target_count = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.gridmatrix[i][j].property == GridProperty.land:
                    self.landsArray.append(position(j, i))
                elif self.gridmatrix[i][j].property == GridProperty.river:
                    self.riverArray.append(position(j, i))
                elif self.gridmatrix[i][j].property == GridProperty.trap:
                    self.trapsArray.append(position(j, i))
                elif self.gridmatrix[i][j].property == GridProperty.target and target_count == 0:
                    self.target = position(j, i)
                    target_count += 1
                elif self.gridmatrix[i][j].property == GridProperty.target and target_count > 0:
                    self.gridmatrix[i][j].property = GridProperty.land
                    self.landsArray.append(position(j, i))
                    target_count += 1

    def detail(self):
        """
        打印Map信息
        """
        print("The map is " + str(self.rows) + "x" + str(self.columns))
        # print("num of trap:" + str(self.num_of_traps))
        # grid_info = ""
        # for i in range(self.rows):
        #     for j in range(self.columns):
        #         grid_info += "(" + str(j) + "," + str(i) + ")" + self.gridmatrix[i][j].detail()
        #     grid_info += "\n"
        # print(grid_info)
