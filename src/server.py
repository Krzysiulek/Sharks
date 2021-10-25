from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .SimpleContinuousModule import SimpleCanvas
from src.agents_factory import AgentsFactory

def shoal_draw(agent):
    return {"Shape": "circle",
            "r": agent.fish_amount / 4,
            "Filled": "true",
            "Color": "#00BFB2"
            }


boid_canvas = SimpleCanvas(shoal_draw, 500, 500)
model_params = {
    "shoal_population": UserSettableParameter("slider", "Ile ławic?", 4, 1, 20, 1),
    "shoal_min_value": UserSettableParameter("slider", "Min. ilość ryb w ławicy", 10, 1, 1000, 1),
    "shoal_max_value": UserSettableParameter("slider", "Max. ilość ryb w ławicy", 100, 2, 1000, 1),
    "width": 100,
    "height": 100,
    "speed": 1,
    "vision": 10,
    "separation": 2,
}

server = ModularServer(AgentsFactory, [boid_canvas], "Sharks", model_params)
