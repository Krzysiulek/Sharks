import numpy as np
from mesa import Agent

from src.agents.swimming_service import get_new_random_velocity


class SharkAgent(Agent):

    def __init__(self,
                 unique_id,
                 model,
                 pos,
                 speed,
                 velocity,
                 vision):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.vision = vision

    def step(self):
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        new_pos = self.pos + get_new_random_velocity(current_velocity=self.velocity, speed=self.speed)
        self.model.space.move_agent(self, new_pos)
