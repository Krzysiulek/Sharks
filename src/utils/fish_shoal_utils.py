import math


def get_fish_r(fish_amount):
    PI = 3.14159

    if fish_amount > 0:
        return math.sqrt(fish_amount / PI)
    else:
        return 0
