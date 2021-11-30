import numpy as np
from mesa import Agent

from src.agents.fish_shoal_agent import FishShoalAgent
from src.utils.fish_shoal_utils import get_fish_r
from src.utils.swimming_service import get_new_random_position, get_new_position_to_object


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

        self.shark_friend_id = None
        self.shark_friend_pos = None

        self.life_amount = 100
        self.fish_vision = 50

        self.age_ctr = 0

    def step(self):
        self.age_ctr += 1

        fish_neighs = self.get_neighbors_fish(self.fish_vision)
        is_fish_eatable = False

        for shoal in fish_neighs:
            tmp_vision = get_fish_r(shoal.fish_amount) / 4
            tmp_fishes = self.get_neighbors_fish(tmp_vision)
            close_enough = len(tmp_fishes) > 0

            if close_enough is True:
                is_fish_eatable = True
                self.fish_to_eat = tmp_fishes[0]
                break

        if (is_fish_eatable):
            self.eat_fish()

        has_shark_friend = self.shark_friend_id is not None

        if has_shark_friend:
            my_sharks = self.get_my_sharks(500)
            if len(my_sharks) == 0:
                has_shark_friend = False
                self.shark_friend_id = None
                self.shark_friend_pos = None
            else:
                self.shark_friend_pos = my_sharks[0].pos


        if has_shark_friend is True:
            self.life_amount -= 0.3
            new_pos = get_new_position_to_object(speed=self.speed,
                                                 target_position=self.pos,
                                                 destination_position=self.shark_friend_pos)
        else:
            self.life_amount -= 1
            new_pos = get_new_random_position(speed=self.speed,
                                              target_position=self.pos)

        self.model.space.move_agent(self, new_pos)

        if self.is_dead():
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)

    def is_dead(self):
        return self.life_amount <= 0

    def eat_fish(self):
        self.life_amount += 2
        self.fish_to_eat.fish_amount -= 1


    def get_my_sharks(self, vision):
        from src.agents.shark_agent import SharkAgent

        neighs = self.model.space.get_neighbors(self.pos, vision, False)
        return [shark for shark in neighs if type(shark) is SharkAgent and shark.unique_id == self.shark_friend_id]


    def get_neighbors_fish(self, vision):
        neighs = self.model.space.get_neighbors(self.pos, vision, False)
        return [x for x in neighs if type(x) is FishShoalAgent and x.fish_amount > 0]