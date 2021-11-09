import numpy as np
from mesa import Agent

from src.agents.fish_shoal_agent import FishShoalAgent
from src.agents.pilot_fish_agent import PilotFishAgent
from src.utils.fish_shoal_utils import get_fish_r
from src.utils.shark_movement_decision import SharkMovementDecision
from src.utils.swimming_service import get_new_position_to_object, get_new_random_position

MAX_LIFE_AMOUNT = 50
HUNGER_LEVEL = 25
ITERATION_LIFE_DECREASE = 1
EATEN_FISH_LIFE_GAIN = 2


class SharkAgent(Agent):

    def __init__(self,
                 unique_id,
                 model,
                 pos,
                 speed,
                 blood_vision,
                 fish_vision):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.blood_vision = blood_vision
        self.fish_vision = fish_vision
        self.pilot_vision = 100

        self.life_amount = MAX_LIFE_AMOUNT
        self.hungry = False

        self.fish_to_eat = None
        self.prev_position = None
        self.my_pilots_amount = 0

    def step(self):
        self.fish_to_eat = None
        new_pos = self.pos
        self.check_is_hungry()
        self.update_my_pilots()

        movement_decision = self.get_movement_decision()

        if movement_decision is SharkMovementDecision.EAT_FISH and self.fish_to_eat.fish_amount > 0:
            self.eat_fish()
        elif movement_decision is SharkMovementDecision.MOVE_TO_BLOOD:
            # płyń do najbliższej krwi
            pass
        elif movement_decision is SharkMovementDecision.MOVE_TO_FISH:
            nearest_fish = self.get_neighbors_fish(self.fish_vision)[0]
            new_pos = get_new_position_to_object(speed=self.speed,
                                                 target_position=self.pos,
                                                 destination_position=nearest_fish.pos)
        else:
            new_pos = get_new_random_position(speed=self.speed,
                                              target_position=self.pos)

        self.model.space.move_agent(self, new_pos)
        if self.is_dead():
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)

    def get_movement_decision(self):
        is_fish_eatable = False
        fish_neighs = self.get_neighbors_fish(self.fish_vision)

        for shoal in fish_neighs:
            tmp_vision = get_fish_r(shoal.fish_amount) / 4
            tmp_fishes = self.get_neighbors_fish(tmp_vision)
            close_enough = len(tmp_fishes) > 0

            if close_enough is True:
                is_fish_eatable = True
                self.fish_to_eat = tmp_fishes[0]
                break

        is_fish_in_vision = len(fish_neighs) > 0
        is_blood_in_vision = len(self.get_neighbors_fish(self.blood_vision)) > 0

        if self.hungry and is_fish_eatable:
            return SharkMovementDecision.EAT_FISH
        elif self.hungry and is_fish_in_vision:
            return SharkMovementDecision.MOVE_TO_FISH
        elif self.hungry and is_blood_in_vision and False:  # todo
            return SharkMovementDecision.MOVE_TO_BLOOD
        else:
            return SharkMovementDecision.MOVE_RANDOMLY

    def get_neighbors_fish(self, vision):
        neighs = self.model.space.get_neighbors(self.pos, vision, False)
        return [x for x in neighs if type(x) is FishShoalAgent and x.fish_amount > 0]

    def get_neighbors_pilots(self, vision):
        neighs = self.model.space.get_neighbors(self.pos, vision, False)
        return [x for x in neighs if type(x) is PilotFishAgent]

    def check_is_hungry(self):
        life_descrease = ITERATION_LIFE_DECREASE - ITERATION_LIFE_DECREASE * self.my_pilots_amount / 5
        self.life_amount -= max(life_descrease, 0.1)

        if self.life_amount < HUNGER_LEVEL:
            self.hungry = True

        if self.life_amount >= MAX_LIFE_AMOUNT:
            self.hungry = False

    def is_dead(self):
        return self.life_amount <= 0

    def eat_fish(self):
        self.life_amount += EATEN_FISH_LIFE_GAIN
        self.fish_to_eat.fish_amount -= 1

    def remove_myself(self):
        self.model.space.remove_agent(self)
        self.model.schedule.remove(self)

    def update_my_pilots(self):
        all_pilots = self.get_neighbors_pilots(self.pilot_vision)
        non_pilots = [pilot for pilot in all_pilots if pilot.shark_friend_id is None]
        my_pilots = [pilot for pilot in all_pilots if pilot.shark_friend_id == self.unique_id]
        self.my_pilots_amount = len(my_pilots)

        ctr = 0
        for pilot in non_pilots:
            if ctr >= 5 - len(my_pilots):
                break

            print("DUPA")
            pilot.shark_friend_id = self.unique_id
            ctr += 1
