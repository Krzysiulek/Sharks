# todo wydzielić logikę od pływania
# todo metody dla rekina, przynawka, ławicy
import random

def get_new_random_velocity(current_velocity, speed):
    start_range = -1
    stop_range = 1

    x_velocity = current_velocity[0] + random.uniform(start_range, stop_range)
    y_velocity = current_velocity[1] + random.uniform(start_range, stop_range)

    x_velocity = get_value_between(-1, 1, x_velocity)
    y_velocity = get_value_between(-1, 1, y_velocity)

    return [x_velocity * speed, y_velocity * speed]


def get_value_between(min_value: float, max_value: float, value: float):
    return min(max_value, max(min_value, value))
