import sys
import os
import numpy as np
from PIL import Image
from functools import reduce
from statistics import median_low


class ImageReader(object):

    def __init__(self, path):
        self.path = path
        self.image = Image.open(self.path)

    def read(self):
        arr = np.array(self.image)

        nrows, ncols = arr.shape
        h_blocks = median_low(self.factors(ncols))
        v_blocks = median_low(self.factors(nrows))
        block_width = ncols // h_blocks
        block_height = nrows // v_blocks

        print("Colors\n{}".format("=" * 6))
        colors = self.image.getcolors()
        for num, color_idx in colors:
            print("{}: {} blocks".format(color_idx, num))

        heading = "{}x{} blocks".format(ncols, nrows)
        print("\n" + heading + "\n" + "=" * len(heading))
        print(self.format_portion_blocks(arr, block_width, block_height))

        for i in range(0, h_blocks):
            for j in range(0, v_blocks):
                heading = "{},{} ({}x{} blocks)".format(i + 1, j + 1, block_width, block_height)
                print("\n" + heading + "\n" + "=" * len(heading))
                p = self.get_portion(arr, i * block_width, j * block_height, block_width, block_height)
                print(self.format_portion(p))

    def get_portion(self, source, x, y, w, h):
        data = np.zeros((w, h), dtype=np.uint8)

        for row_idx in range(x, x + w):
            for col_idx in range(y, y + h):
                data[row_idx - x][col_idx - y] = source[row_idx][col_idx]

        return data

    def format_portion(self, section):
        rows = []
        for row_idx in range(0, len(section)):
            rows.append(" ".join(map(lambda x: str(x), section[row_idx])))
        return "\n".join(rows)

    def format_portion_blocks(self, section, block_width, block_height):
        rows = []
        for row_idx in range(0, len(section)):
            row = []
            for col_idx in range(0, len(section[row_idx])):
                if col_idx and col_idx % block_width == 0:
                    row.append(" = " if section[row_idx][col_idx] == section[row_idx][col_idx - 1] else "   ")

                row.append(str(section[row_idx][col_idx]))

            if row_idx and row_idx % block_width == 0:
                extra_row = []
                rows.append("")

                for col_idx in range(0, len(section[row_idx])):
                    if col_idx and col_idx % block_width == 0:
                        extra_row.append("   ")

                    extra_row.append("‖" if section[row_idx][col_idx] == section[row_idx - 1][col_idx] else " ")

                rows.append(" ".join(extra_row))
                rows.append("")

            rows.append(" ".join(row))
        return "\n".join(rows)

    @staticmethod
    def factors(n):
        return set(reduce(
            list.__add__,
            ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0)
        ))

    def write(self, image):
        filename, ext = os.path.splitext(self.path)
        image.save(filename + ".mod.png", "PNG")


if __name__ == "__main__":

    ir = ImageReader(path=sys.argv[1])
    ir.read()
