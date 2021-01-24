import colorsys
import numpy as np

def generate_colors(class_num):
    hsv_tuples = [(x / class_num, 1., 1.) for x in range(class_num)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(
        map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
    np.random.seed(10101)
    np.random.shuffle(colors) 

    return colors