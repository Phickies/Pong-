from game_manager import GameManager


def main():

    game = GameManager(window_size=(800, 505))

    while True:
        game.event_handle()
        game.update()
        game.display()


if __name__ == '__main__':
    main()
