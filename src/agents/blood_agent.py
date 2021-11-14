import numpy as np
from mesa import Agent

MAX_BLOOD_RADIUS = 50


class BloodAgent(Agent):

    def __init__(self,
                 unique_id,
                 model,
                 pos,
                 radius=1):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.radius = radius

    def step(self):
        self.radius += 1

        if self.radius >= MAX_BLOOD_RADIUS:
            self.remove_myself()

    def remove_myself(self):
        self.model.space.remove_agent(self)
        self.model.schedule.remove(self)
