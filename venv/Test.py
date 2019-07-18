from Board import Board


def main():
    board = Board()
    board.populate_left_move()
    board.print_board()
    board.add_random()
    board.print_board()
    board.add_random()
    board.print_board()



if __name__ == "__main__":
    main()

