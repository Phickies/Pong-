from game_manager import GameManager


def main():

    game = GameManager(window_size=(800, 505))

    while True:
        game.run_loop()


if __name__ == '__main__':
    main()
