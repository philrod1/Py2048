from Board import Board


def main():
    board = Board()
    board.populate_left_move()
    for v in range(0, 0xFFFF + 1):
        print('%04X => %04X' % (v, board.reverse_row(v)))


if __name__ == "__main__":
    main()

