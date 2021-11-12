import uuid

from Base import AnimalStatus, position


class Animal(object):
    """
    动物类，游戏中所有动物的父类，这里会定义一些所有动物都共有的属性和方法

    Attributes:
        type:物种
        pos：当前位置
        status:是否存活
        Combat_Effectiveness：战斗值，同一个物种不同个体，通过比较战斗值高低决胜
        id:每个动物的id，用于从花名册中查询
    """
    type: str
    pos: position
    status: AnimalStatus
    Combat_Effectiveness: float
    id: uuid

    def __init__(self, pos):
        """
        创建一个动物，我们首先需要给他一个初始的位置
        然后让它活着（alive)

        :param pos: 位置
        :return:
        """
        self.pos = pos
        self.status = AnimalStatus.alive
        # 随机生成一个id
        self.id = uuid.uuid1()

    def move(self, delta_x: int, delta_y: int):
        """
        移动动物，让动物跑起来

        :param delta_x: x方向跑了多远
        :param delta_y: y方向跑了多远
        :return:
        """
        self.pos.move(delta_x, delta_y)

    def wasHunted(self):
        """
        动物被天敌吃掉了（大象吃老虎，老虎吃老鼠，老鼠吃大象。。。）
        这时候它的状态就从alive变成了dead

        :return:
        """
        self.status = AnimalStatus.dead

    def getTrapped(self):
        """
        动物掉进了陷阱里，"洞化"了

        :return:
        """
        self.status = AnimalStatus.dead

    def common_detail(self):
        """
        打印动物共有属性

        Returns:

        """
        print("type:" + self.type)
        print("id:" + str(self.id))
        print("pos:" + self.pos.detail())
        print("combat effectiveness:" + str(self.Combat_Effectiveness))
        print("-----------------------------------------\n")
