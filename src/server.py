from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from src.agents_factory import AgentsFactory
from .SimpleContinuousModule import SimpleCanvas
from .agents.fish_shoal_agent import FishShoalAgent
from .agents.shark_agent import SharkAgent
from .utils.fish_shoal_utils import get_fish_r


def draw_agent(agent):
    if type(agent) is FishShoalAgent:
        return shoal_draw(agent)
    elif type(agent) is SharkAgent:
        return shark_draw(agent)

def shoal_draw(agent):
    return {
        "Shape": "circle",
        "r": get_fish_r(agent.fish_amount),
        "Filled": "true",
        "Color": "#00BFB2"
    }

def shark_draw(agent):
    return {
        "Shape": "circle",
        "r": 1,
        "Filled": "true",
        "Color": "#4D5C9E"
    }


boid_canvas = SimpleCanvas(draw_agent, 500, 500)
model_params = {
    # shoal
    "shoal_population": UserSettableParameter("slider", "Ile ławic?", 4, 1, 20, 1),
    "shoal_speed": UserSettableParameter("slider", "Szybkość ławicy", 1, 1, 25, 1),
    "shoal_min_value": UserSettableParameter("slider", "Min. ilość ryb w ławicy", 10, 1, 1000, 1),
    "shoal_max_value": UserSettableParameter("slider", "Max. ilość ryb w ławicy", 100, 2, 1000, 1),
    # shark
    "sharks_population": UserSettableParameter("slider", "Ile rekinów?", 4, 1, 100, 1),
    "shark_speed": UserSettableParameter("slider", "Szybkość rekina", 2, 1, 25, 1),
    "shark_blood_vision": 200,
    "shark_fish_vision": 20,
    # other
    "width": 100,
    "height": 100,
    "vision": 10,
    "separation": 2,
}

server = ModularServer(AgentsFactory, [boid_canvas], "Sharks", model_params)
