import numpy as np
from mesa import Agent

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
                 cohere=0.025,
                 separate=0.25,
                 match=0.04,
                 fish_amount=100):
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
        self.velocity /= np.linalg.norm(self.velocity)

        new_pos = self.pos + get_new_random_velocity(current_velocity=self.velocity, speed=self.speed)
        self.model.space.move_agent(self, new_pos)
