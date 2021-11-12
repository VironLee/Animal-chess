from Animal_chess import Animal_chess
from Base import Map, position
from Global import animal_dict
from tiger import Tiger

if __name__ == "__main__":
    # # 生成默认地图
    # map1 = Map.generate_default_map()
    # map1.detail()
    #
    # # 新建一个老虎对象
    # tiger_1 = Tiger(position(1, 2))
    # tiger_2 = Tiger(position(2, 2))
    #
    # print("直接访问老虎的信息\n")
    # tiger_1.detail()
    # tiger_2.detail()
    #
    # animal_dict[tiger_1.id] = tiger_1
    # animal_dict[tiger_2.id] = tiger_2
    #
    # # 把老虎放到地图上
    # map1.put_animal(position(3, 1), tiger_1.id)
    # map1.put_animal(position(8, 6), tiger_2.id)
    #
    # #打印此刻map信息，看看动物的位置是否正确
    # map1.detail()

    animal_chess=Animal_chess.create_random_game()

