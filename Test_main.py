from Animal_chess import Animal_chess


def animal_move_test(game: Animal_chess) -> bool:
    score = 0
    score += int(game.move_test("rat", "land", 1))
    score += int(game.move_test("rat", "river", 2) * 10)
    score += int(game.move_test("rat", "trap", 3) * 100)
    score += int(game.move_test("rat", "target", 4) * 1000)  ### 测试3与测试4顺序有误，出现动物跑到陷阱里不影响下一测试结果的情况

    if score == 1111:
        print("Congratulation!You have completed move functions!")
        return True
    else:
        print("Move test score is" + str(score) + ".It seems there are some bugs in your code. Find and kill them all!")

    return True


def animal_battle_test(game: Animal_chess) -> bool:
    score = 0
    score += int(game.battle_test("rat", "rat", 1))
    score += int(game.battle_test("rat", "tiger", 2)) * 10
    score += int(game.battle_test("rat", "elephant", 3)) * 100
    score += int(game.battle_test("tiger", "rat", 4)) * 1000
    score += int(game.battle_test("tiger", "tiger", 5)) * 10000
    score += int(game.battle_test("tiger", "elephant", 6)) * 100000
    score += int(game.battle_test("elephant", "rat", 7)) * 1000000
    score += int(game.battle_test("elephant", "tiger", 8)) * 10000000
    score += int(game.battle_test("elephant", "elephant", 9)) * 100000000

    if score == 111111111:
        print("Congratulation!You have completed battle functions!")
        return True
    else:
        print("Battle test score is " + str(
            score) + ".It seems there are some bugs in your code. Find and kill them all!")
    return True


if __name__ == "__main__":
    animal_chess = Animal_chess.create_test_game()

    # TODO:完成Test move:
    if animal_move_test(animal_chess):
        # TODO:完成Test move:
        animal_battle_test(animal_chess)
