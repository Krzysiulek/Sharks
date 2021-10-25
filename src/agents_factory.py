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

from src.agents.fish_shoal_agent import FishShoalAgent
from src.agents.shark_agent import SharkAgent


class AgentsFactory(Model):
    def __init__(
        self,
        shoal_population=1000,
        shoal_speed=1,
        shoal_min_value=1,
        shoal_max_value=2,
        sharks_population=1,
        width=100,
        height=100,
        speed=1,
        vision=10,
        separation=2,
        cohere=0.025,
        separate=0.25,
        match=0.04,
    ):
        # shoal
        self.shoal_population = shoal_population
        self.shoal_min_value = shoal_min_value
        self.shoal_max_value = shoal_max_value
        self.shoal_speed = shoal_speed

        # sharks
        self.sharks_population = sharks_population

        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        self.factors = dict(cohere=cohere, separate=separate, match=match)

        self.unique_id_iterator = 0
        self.make_agents()
        self.running = True

    def make_agents(self):
        self.make_shoals()
        self.make_sharks()

    # todo ladniej to zrobic, bo straszy ta funkcja i kolejna
    def make_shoals(self):
        for _ in range(self.shoal_population):
            self.unique_id_iterator += 1
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            fish_amount = np.random.randint(low=self.shoal_min_value, high=self.shoal_max_value, size=1)[0]
            shoal_agent = FishShoalAgent(
                self.unique_id_iterator,
                self,
                pos,
                self.shoal_speed,
                velocity,
                self.vision,
                self.separation,
                **self.factors,
                fish_amount=fish_amount
            )
            self.space.place_agent(shoal_agent, pos)
            self.schedule.add(shoal_agent)

    def make_sharks(self):
        for _ in range(self.sharks_population):
            self.unique_id_iterator += 1
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            shark = SharkAgent(
                self.unique_id_iterator,
                self,
                pos,
                self.speed,
                velocity,
                self.vision,
            )
            self.space.place_agent(shark, pos)
            self.schedule.add(shark)

    def step(self):
        self.schedule.step()
