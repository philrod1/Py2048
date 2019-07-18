import random


class Board:

    bin_grid = [
        0x0000,
        0x0000,
        0x0000,
        0x0000
    ]

    left_moves = {}

    def populate_left_move(self):
        self.left_moves[0] = 0

        for v in range(1, 0xFFFF+1):

            d = v & 0xF
            c = (v >> 4) & 0xF
            b = (v >> 8) & 0xF
            a = (v >> 12) & 0xF

            i = 0
            while a == 0 and i < 3:
                a = b
                b = c
                c = d
                d = 0
                i += 1

            i = 0
            while b == 0 and i < 2:
                b = c
                c = d
                d = 0
                i += 1

            if c == 0:
                c = d
                d = 0

            if a == b:
                a = ((a + 1) & 0xF)
                b = c
                c = d
                d = 0

            if b + c == 0:
                value = (a << 12) | (b << 8) | (c << 4) | d
            else:
                while b == 0:
                    b = c
                    c = d
                    d = 0

                if b == c:
                    b = ((b + 1) & 0xF)
                    c = d
                    d = 0

                if c == 0:
                    value = (a << 12) | (b << 8) | (c << 4) | d
                else:
                    if c == d:
                        c = ((c + 1) & 0xF)
                        d = 0
                    value = ((a << 12) | (b << 8) | (c << 4) | d)

            self.left_moves[v] = value
            # print('%04X => %04X' % (v, value))

    def reverse_row(self, row):
        rev = 0
        rev |= (row & 0x000F) << 12
        rev |= (row & 0x00F0) << 4
        rev |= (row & 0x0F00) >> 4
        rev |= (row & 0xF000) >> 12
        return rev