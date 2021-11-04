import numpy as np
from mesa import Agent
import random

from src.agents.swimming_service import get_new_random_velocity


class FishShoalAgent(Agent):

    def __init__(self,
                 unique_id,
                 model,
                 pos,
                 speed,
                 velocity,
                 vision,
                 separation,
                 fish_amount=100):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.vision = vision
        self.separation = separation

        # liczba ryb w ławicy
        self.fish_amount = fish_amount

    def step(self):
        self.reproduce_myself()
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        self.velocity /= np.linalg.norm(self.velocity)

        new_pos = self.pos + get_new_random_velocity(current_velocity=self.velocity, speed=self.speed)
        self.model.space.move_agent(self, new_pos)


    def reproduce_myself(self):
        reproduction_rate = 0.001
        for _ in range(0, self.fish_amount):
            if random.random() <= reproduction_rate:
                self.fish_amount += 1
