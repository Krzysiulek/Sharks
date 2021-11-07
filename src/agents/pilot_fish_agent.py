import numpy as np
from mesa import Agent

from src.utils.swimming_service import get_new_random_position


class PilotFishAgent(Agent):

    def __init__(self,
                 unique_id,
                 model,
                 pos,
                 speed,
                 vision):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.vision = vision

    def step(self):
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        new_pos = get_new_random_position(speed=self.speed,
                                          target_position=self.pos)
        self.model.space.move_agent(self, new_pos)
