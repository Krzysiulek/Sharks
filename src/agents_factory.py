"""
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""

import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
import random

from src.agents.blood_agent import BloodAgent
from src.agents.fish_shoal_agent import FishShoalAgent
from src.agents.pilot_fish_agent import PilotFishAgent
from src.agents.shark_agent import SharkAgent


class AgentsFactory(Model):
    def __init__(self,
                 shoal_population=1000,
                 shoal_speed=1,
                 shoal_min_value=1,
                 shoal_max_value=2,
                 sharks_population=1,
                 pilots_population=1,
                 shark_speed=1,
                 shark_blood_vision=1,
                 shark_fish_vision=1,
                 pilot_vision=1,
                 width=100,
                 height=100,
                 vision=100,
                 separation=2):
        global AREA_HEIGHT, AREA_WIDTH
        AREA_HEIGHT = height
        AREA_WIDTH = width

        # shoal
        self.shoal_population = shoal_population
        self.shoal_min_value = shoal_min_value
        self.shoal_max_value = shoal_max_value
        self.shoal_speed = shoal_speed

        # sharks
        self.sharks_population = sharks_population
        self.shark_speed = shark_speed
        self.shark_blood_vision = shark_blood_vision
        self.shark_fish_vision = shark_fish_vision

        # pilots
        self.pilot_speed = shark_speed
        self.pilot_vision = pilot_vision
        self.pilots_population = pilots_population

        # todo do posprzątania
        self.vision = vision
        self.separation = separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, True)
        self.datacollector = DataCollector(
            {
                "Fish": lambda m: self.get_all_fish_amount(),
                "Sharks": lambda m: self.get_all_sharks_amount(),
                "Shoal": lambda m: self.get_all_shoal_amount(),
                "Pilots": lambda m: self.get_all_pilots_amount(),
                "Average_Shark_Life_Amount": lambda m: self.get_average_shark_life(),
                "Average_Pilot_Life_Amount": lambda m: self.get_average_pilot_life(),
                "Average_Shark_Life_Lenght": lambda m: self.get_average_shark_life_len(),
                "Average_Pilot_Life_Lenght": lambda m: self.get_average_pilot_life_len(),
                "Average_Pilot_Amount_Per_Shark": lambda m: self.get_average_pilot_amount_per_shark(),
            }
        )

        self.unique_id_iterator = 0
        self.make_agents()
        self.datacollector.collect(self)
        self.running = True

    def make_agents(self):
        self.make_shoals()
        self.make_sharks()
        self.make_pilots()


    def make_shoals(self):
        for _ in range(self.shoal_population):
            self.create_new_shoal()

    def make_sharks(self):
        for _ in range(self.sharks_population):
            self.create_new_shark()

    def make_pilots(self):
        for _ in range(self.pilots_population):
            self.create_new_pilot_fish()

    def step(self):
        self.reproduce_new_shoal()
        self.reproduce_shark()
        self.reproduce_pilots()
        self.schedule.step()
        self.datacollector.collect(self)

    def get_all_fish_amount(self):
        neighs = self.space.get_neighbors([0, 0], 999999, True)
        fishes = [x for x in neighs if type(x) is FishShoalAgent and x.fish_amount > 0]
        return float(sum([item.fish_amount for item in fishes]))

    def get_all_shoal_amount(self):
        neighs = self.space.get_neighbors([0, 0], 999999, True)
        fishes = [x for x in neighs if type(x) is FishShoalAgent and x.fish_amount > 0]
        return len(fishes)

    def get_all_pilots_amount(self):
        neighs = self.space.get_neighbors([0, 0], 999999, True)
        fishes = [x for x in neighs if type(x) is PilotFishAgent]
        return len(fishes)

    def get_all_sharks_amount(self):
        neighs = self.space.get_neighbors([0, 0], 999999, True)
        fishes = [x for x in neighs if type(x) is SharkAgent]
        return len(fishes)

    def get_average_shark_life(self):
        neighs = self.space.get_neighbors([0, 0], 999999, True)
        fishes = [x for x in neighs if type(x) is SharkAgent]

        fishes_amount = len(fishes)
        lifes_amount = 0

        for fish in fishes:
            lifes_amount += fish.life_amount

        if fishes_amount != 0:
            return lifes_amount / fishes_amount

        return 0

    def get_average_pilot_life(self):
        neighs = self.space.get_neighbors([0, 0], 999999, True)
        fishes = [x for x in neighs if type(x) is PilotFishAgent]

        fishes_amount = len(fishes)
        lifes_amount = 0

        for fish in fishes:
            lifes_amount += fish.life_amount

        if fishes_amount != 0:
            return lifes_amount / fishes_amount

        return 0

    def get_average_shark_life_len(self):
        neighs = self.space.get_neighbors([0, 0], 999999, True)
        fishes = [x for x in neighs if type(x) is SharkAgent]
        fishes_amount = len(fishes)

        lifes_amount = 0
        for fish in fishes:
            lifes_amount += fish.age_ctr


        if fishes_amount != 0:
            return lifes_amount / fishes_amount

        return 0

    def get_average_pilot_life_len(self):
        neighs = self.space.get_neighbors([0, 0], 999999, True)
        fishes = [x for x in neighs if type(x) is PilotFishAgent]
        fishes_amount = len(fishes)

        lifes_amount = 0
        for fish in fishes:
            lifes_amount += fish.age_ctr

        if fishes_amount != 0:
            return lifes_amount / fishes_amount

        return 0


    def get_average_pilot_amount_per_shark(self):
        neighs = self.space.get_neighbors([0, 0], 999999, True)
        fishes = [x for x in neighs if type(x) is SharkAgent]

        fishes_amount = len(fishes)
        pilots_amount = 0

        for fish in fishes:
            pilots_amount += fish.my_pilots_amount

        if fishes_amount != 0:
            return pilots_amount / fishes_amount

        return 0

    def reproduce_shark(self):
        reproduction_rate = 0.0025
        for _ in range(0, self.get_all_sharks_amount()):
            if random.random() <= reproduction_rate:
                self.create_new_shark()


    def reproduce_pilots(self):
        reproduction_rate = 0.001
        for _ in range(0, self.get_all_pilots_amount()):
            if random.random() <= reproduction_rate:
                self.create_new_pilot_fish()

    def reproduce_new_shoal(self):
        reproduction_rate = 0.005
        if random.random() <= reproduction_rate:
            self.create_new_shoal()

    def create_new_shark(self):
        self.unique_id_iterator += 1
        x = self.random.random() * self.space.x_max
        y = self.random.random() * self.space.y_max
        pos = np.array((x, y))
        shark = SharkAgent(unique_id=self.unique_id_iterator,
                           model=self,
                           pos=pos,
                           speed=self.shark_speed,
                           blood_vision=self.shark_blood_vision,
                           fish_vision=self.shark_fish_vision)
        self.space.place_agent(shark, pos)
        self.schedule.add(shark)

    def create_new_shoal(self):
        self.unique_id_iterator += 1
        x = self.random.random() * self.space.x_max
        y = self.random.random() * self.space.y_max
        pos = np.array((x, y))
        velocity = np.random.random(2) * 2 - 1
        fish_amount = np.random.randint(low=self.shoal_min_value, high=self.shoal_max_value, size=1)[0]

        shoal_agent = FishShoalAgent(self.unique_id_iterator,
                                     self,
                                     pos,
                                     self.shoal_speed,
                                     velocity,
                                     self.vision,
                                     self.separation,
                                     fish_amount=fish_amount)
        self.space.place_agent(shoal_agent, pos)
        self.schedule.add(shoal_agent)

    def create_new_pilot_fish(self):
        self.unique_id_iterator += 1
        x = self.random.random() * self.space.x_max
        y = self.random.random() * self.space.y_max
        pos = np.array((x, y))
        pilot_agent = PilotFishAgent(unique_id=self.unique_id_iterator,
                                     model=self,
                                     pos=pos,
                                     speed=self.pilot_speed,
                                     vision=self.pilot_vision)
        self.space.place_agent(pilot_agent, pos)
        self.schedule.add(pilot_agent)

    def create_blood(self, pos):
        self.unique_id_iterator += 1
        pilot_agent = BloodAgent(unique_id=self.unique_id_iterator,
                                 model=self,
                                 pos=pos,
                                 max_radius=self.shark_blood_vision,
                                 radius=1)
        self.space.place_agent(pilot_agent, pos)
        self.schedule.add(pilot_agent)
