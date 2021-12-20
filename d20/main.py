from typing import List

import numpy as np


def enhance(padded_img: np.ndarray, iea: List[int]):
    new_image = padded_img.copy()
    for i in range(1, padded_img.shape[0] - 1):
        for j in range(1, padded_img.shape[1] - 1):
            key = "".join(str(n) for n in padded_img[i - 1, j - 1:j + 2])
            key += "".join(str(n) for n in padded_img[i, j - 1:j + 2])
            key += "".join(str(n) for n in padded_img[i + 1, j - 1:j + 2])
            key_value = int(key, base=2)
            new_image[i, j] = iea[key_value]
    return new_image


def pretty_print_image(image: np.ndarray):
    print("~~~~~~~~~~~~~~~~~~~~")
    for i in range(image.shape[0]):
        print("".join(['#' if image[i][j] == 1 else '.' for j in range(image.shape[1])]))
    print("~~~~~~~~~~~~~~~~~~~~")


def main():
    with open("input", 'r') as fd:
        lines = fd.readlines()
        iea = [1 if char == '#' else 0 for char in lines[0].strip()]
        image_input = [list(line.strip()) for line in lines[2:]]

        padded_img = np.array(image_input)

        padded_img[padded_img == '.'] = 0
        padded_img[padded_img == '#'] = 1

        padded_img = np.pad(padded_img, 4, constant_values=0).astype(np.int8)

        padded_img = enhance(padded_img, iea)[1:-1, 1:-1]
        padded_img = enhance(padded_img, iea)[1:-1, 1:-1]

        pretty_print_image(padded_img)
        print("non-zero elems:", np.count_nonzero(padded_img))


if __name__ == "__main__":
    main()
