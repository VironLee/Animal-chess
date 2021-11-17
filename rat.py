from animal import Animal


class Rat(Animal):
    x: int
    y: int

    # 2.所以我在老鼠类中覆写了父类控制坐标的方法，用x和y两个变量代替Animal中的pos
    def __init__(self, pos, x, y):
        Animal.__init__(self, pos)
        self.x = x
        self.y = y

    def move(self, delta_x, delta_y):
        self.x += 2 * delta_x
        self.y += 2 * delta_y

    def des(self):
        print("Rat's destination is (%d, %d)" % (self.x, self.y))
        # 进行了输出坐标的优化
