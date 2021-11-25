from Animal_chess import Animal_chess


def animal_move_test(game: Animal_chess):
    score = 0;
    score += int(game.move_test("rat", "land", 1))
    score += int(game.move_test("rat", "river", 2) * 10)
    score += int(game.move_test("rat", "trap", 3) * 100)
    score += int(game.move_test("rat", "target", 4) * 1000)

    if score == 1111:
        print("Congradulation!You have completed move fucntions!")
    else:
        print("Move test score is" + str(score) + ".It seems there are some bugs in your code. Find and kill them all!")


def animal_battle_test(game: Animal_chess):
    score = 0
    score += int(game.battle_test("rat", "rat", 1))
    score += int(game.battle_test("rat", "tiger", 2))
    score += int(game.battle_test("rat", "elephant", 3))
    score += int(game.battle_test("tiger", "rat", 4))
    score += int(game.battle_test("tiger", "tiger", 5))
    score += int(game.battle_test("tiger", "elephant", 6))
    score += int(game.battle_test("elephant", "rat", 7))
    score += int(game.battle_test("elephant", "tiger", 8))
    score += int(game.battle_test("elephant", "elephant", 9))

    if score == 111111111:
        print("Congradulation!You have completed battle fucntions!")
    else:
        print("Battle test score is " + str(
            score) + ".It seems there are some bugs in your code. Find and kill them all!")


if __name__ == "__main__":
    animal_chess = Animal_chess.create_random_game()

    # TODO:完成Test move:
    if animal_move_test(animal_chess):
        # TODO:完成Test move:
        animal_battle_test(animal_chess)
