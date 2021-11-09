# todo metody dla rekina, przynawka, ławicy
import random, math


def get_new_random_velocity(current_velocity, speed):
    start_range = -1
    stop_range = 1

    x_velocity = current_velocity[0] + random.uniform(start_range, stop_range)
    y_velocity = current_velocity[1] + random.uniform(start_range, stop_range)

    x_velocity = get_value_between(-1, 1, x_velocity)
    y_velocity = get_value_between(-1, 1, y_velocity)

    return [x_velocity * speed, y_velocity * speed]

def get_new_random_position(speed,
                            target_position):
    random_x_point = random.choices(range(int(target_position[0]) - 5, int(target_position[0]) + 10), k=1)[0]
    random_y_point = random.choices(range(int(target_position[1]) - 5, int(target_position[1]) + 10), k=1)[0]

    return get_new_position_to_object(speed, target_position, [random_x_point, random_y_point])


def get_new_position_to_object(speed, target_position, destination_position):
    target_x = target_position[0]
    target_y = target_position[1]

    dest_x = destination_position[0]
    dest_y = destination_position[1]

    big_z = math.sqrt(pow(dest_x - target_x, 2) + pow(dest_y - target_y, 2))
    big_a = dest_x - target_x
    big_b = dest_y - target_y

    small_a = (speed * big_a) / big_z
    small_b = (speed * big_b) / big_z

    return [target_position[0] + small_a, target_position[1] + small_b]


def get_value_between(min_value: float, max_value: float, value: float):
    return min(max_value, max(min_value, value))
