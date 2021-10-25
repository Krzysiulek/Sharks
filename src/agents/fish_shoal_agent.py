import random

import numpy as np
from mesa import Agent


class FishShoalAgent(Agent):

    def __init__(
            self,
            unique_id,
            model,
            pos,
            speed,
            velocity,
            vision,
            separation,
            cohere=0.025,
            separate=0.25,
            match=0.04,
            fish_amount=100
    ):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.vision = vision
        self.separation = separation
        self.cohere_factor = cohere
        self.separate_factor = separate
        self.match_factor = match

        # liczba ryb w ławicy
        self.fish_amount = fish_amount

    def step(self):
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        print(self.pos)
        print(self.get_new_velocity())
        print(self.speed)
        print(self.get_new_velocity() * self.speed)
        print(self.pos + self.get_new_velocity())
        print()
        self.velocity /= np.linalg.norm(self.velocity)

        new_pos = self.pos + self.get_new_velocity() * self.speed
        self.model.space.move_agent(self, new_pos)

    # todo ruszanie po plaszy jest zepsute dla speed > 1
    def get_new_velocity(self):
        # todo jesli rekin blisko - uciekaj
        start_range = -0.5
        stop_range = 0.5

        x_velocity = self.velocity[0] + random.uniform(start_range, stop_range)
        y_velocity = self.velocity[1] + random.uniform(start_range, stop_range)

        x_velocity = self.get_value_between(-1, 1, x_velocity)
        y_velocity = self.get_value_between(-1, 1, y_velocity)

        return [x_velocity, y_velocity]

    def get_value_between(self, min_value: float, max_value: float, value: float):
        return min(max_value, max(min_value, value))
