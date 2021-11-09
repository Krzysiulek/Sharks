import numpy as np
from mesa import Agent

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

    def step(self):
        has_shark_friend = self.shark_friend_id is not None
        print("Shark id: " + str(self.shark_friend_id))

        if has_shark_friend:
            my_sharks = self.get_my_sharks(500)
            if len(my_sharks) == 0:
                has_shark_friend = False
                self.shark_friend_id = None
                self.shark_friend_pos = None
            else:
                self.shark_friend_pos = my_sharks[0].pos


        if has_shark_friend is True:
            self.life_amount -= 0.1
            new_pos = get_new_position_to_object(speed=self.speed,
                                                 target_position=self.pos,
                                                 destination_position=self.shark_friend_pos)
            # todo zjada pasozyty
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

    def get_my_sharks(self, vision):
        from src.agents.shark_agent import SharkAgent

        neighs = self.model.space.get_neighbors(self.pos, vision, False)
        return [shark for shark in neighs if type(shark) is SharkAgent and shark.unique_id == self.shark_friend_id]
