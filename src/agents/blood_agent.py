import numpy as np
from mesa import Agent

class BloodAgent(Agent):

    def __init__(self,
                 unique_id,
                 model,
                 pos,
                 max_radius,
                 radius=1):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.radius = radius
        self.max_blood_radius = max_radius

    def step(self):
        self.radius += self.max_blood_radius / 10

        if self.radius >= self.max_blood_radius:
            self.remove_myself()

    def remove_myself(self):
        self.model.space.remove_agent(self)
        self.model.schedule.remove(self)
