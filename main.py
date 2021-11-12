from Base import Map, position
from animal import Animal
from tiger import Tiger

if __name__ == "__main__":
    map1 = Map.generate_default_map()
    map1.detail()

    # 新建一个老虎对象
    pos1=position(1,2)
    pos2=position(2,2)
    animal = Animal(pos2)
    tiger_1 = Tiger(pos1)
    tiger_2 = Tiger(pos2)

    print("直接访问老虎的信息\n")
    tiger_1.detail()
    tiger_2.detail()

    # 新建一个dictionary存储这轮游戏中所有动物的信息，
    # uuid是key，每个动物对象本身是value
    animal_dict={}
    animal_dict[tiger_1.id]=tiger_1
    animal_dict[tiger_2.id]=tiger_2

    print("通过id从花名册中访问老虎的信息(从tiger2 到tiger1)\n")
    animal_dict[tiger_2.id].detail()
    animal_dict[tiger_1.id].detail()

