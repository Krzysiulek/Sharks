import random

import numpy as np
from mesa import Agent


class SharkAgent(Agent):

    def __init__(
            self,
            unique_id,
            model,
            pos,
            speed,
            velocity,
            vision
    ):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.vision = vision

    def step(self):
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        new_pos = self.pos + self.get_new_velocity() * self.speed
        self.model.space.move_agent(self, new_pos)

    # todo zepsuta funkcja dla speed > 1
    # todo parametr shark_speed
    def get_new_velocity(self):
        start_range = -0.5
        stop_range = 0.5

        x_velocity = self.velocity[0] + random.uniform(start_range, stop_range)
        y_velocity = self.velocity[1] + random.uniform(start_range, stop_range)

        x_velocity = self.get_value_between(-1, 1, x_velocity)
        y_velocity = self.get_value_between(-1, 1, y_velocity)

        return [x_velocity, y_velocity]

    def get_value_between(self, min_value: float, max_value: float, value: float):
        return min(max_value, max(min_value, value))
