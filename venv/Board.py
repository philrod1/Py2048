import random


class Board:

    board = 0

    left_moves = {}

    def combine_row(self, a, b, c, d):
        return (a << 12) | (b << 8) | (c << 4) | d

    def split_row(self, row):
        return (row >> 12) & 0xF, (row >> 8) & 0xF, (row >> 4) & 0xF, row & 0xF

    def get_rows(self):
        return [
            (self.board >> 48) & 0xFFFF,
            (self.board >> 32) & 0xFFFF,
            (self.board >> 16) & 0xFFFF,
            self.board & 0xFFFF,
        ]

    def join_rows(self, rows):
        result = 0
        for row in rows:
            row = row << 16
            result |= (row & 0xFFFF)
        return result

    def reverse_row(self, row):
        rev = 0
        rev |= (row & 0x000F) << 12
        rev |= (row & 0x00F0) << 4
        rev |= (row & 0x0F00) >> 4
        rev |= (row & 0xF000) >> 12
        return rev

    def transpose_board(self, board):
        a1 = board & 0xF0F00F0FF0F00F0F
        a2 = board & 0x0000F0F00000F0F0
        a3 = board & 0x0F0F00000F0F0000
        a = a1 | (a2 << 12) | (a3 >> 12)
        b1 = a & 0xFF00FF0000FF00FF
        b2 = a & 0x00FF00FF00000000
        b3 = a & 0x00000000FF00FF00
        return b1 | (b2 >> 24) | (b3 << 24)

    def print_board(self):
        print()
        for row in self.get_rows():
            print('%04X' % row)

    def add_random(self):
        empties = []
        board = self.board
        for i in range(16):
            if (board & 0xF) == 0:
                empties.append(i)
            board >>= 4
        if len(empties) == 0:
            return False
        index = empties.pop(random.randint(0, len(empties)-1))
        p = random.randint(1, 10)
        if p == 1:
            result = 2 << 4 * index
        else:
            result = 1 << 4 * index
        self.board |= result
        return True

    def populate_left_move(self):
        self.left_moves[0] = 0

        for v in range(1, 0xFFFF+1):

            a, b, c, d = self.split_row(v)

            i = 0
            while a == 0 and i < 3:
                a = b; b = c; c = d; d = 0; i += 1

            i = 0
            while b == 0 and i < 2:
                b = c; c = d; d = 0; i += 1

            if c == 0:
                c = d; d = 0

            if a == b:
                a = (a + 1) & 0xF
                b = c; c = d; d = 0

            if b + c == 0:
                value = self.combine_row(a, b, c, d)
            else:
                while b == 0:
                    b = c; c = d; d = 0

                if b == c:
                    b = (b + 1) & 0xF
                    c = d; d = 0

                if c == 0:
                    value = self.combine_row(a, b, c, d)
                else:
                    if c == d:
                        c = (c + 1) & 0xF
                        d = 0
                    value = self.combine_row(a, b, c, d)

            self.left_moves[v] = value
            # print('%04X => %04X' % (v, value))
