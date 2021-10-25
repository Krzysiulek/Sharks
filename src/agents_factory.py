"""
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""

import numpy as np

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

from src.agents.fish_shoal import FishShoal


class AgentsFactory(Model):
    def __init__(
        self,
        shoal_population=1000,
        shoal_min_value=1,
        shoal_max_value=2,
        width=100,
        height=100,
        speed=1,
        vision=10,
        separation=2,
        cohere=0.025,
        separate=0.25,
        match=0.04,
    ):
        self.shoal_population = shoal_population
        self.shoal_min_value = shoal_min_value
        self.shoal_max_value = shoal_max_value

        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        self.factors = dict(cohere=cohere, separate=separate, match=match)
        self.make_agents()
        self.running = True

    def make_agents(self):
        for i in range(self.shoal_population):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            fish_amount = np.random.randint(low=self.shoal_min_value, high=self.shoal_max_value, size=1)[0]
            boid = FishShoal(
                i,
                self,
                pos,
                self.speed,
                velocity,
                self.vision,
                self.separation,
                **self.factors,
                fish_amount=fish_amount
            )
            self.space.place_agent(boid, pos)
            self.schedule.add(boid)

    def step(self):
        self.schedule.step()
