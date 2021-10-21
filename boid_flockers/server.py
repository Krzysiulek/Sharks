from mesa.visualization.ModularVisualization import ModularServer
from .SimpleContinuousModule import SimpleCanvas
from .model import BoidFlockers

SUSPECTIBLE = "SUS"
INFECTED = "INF"
REMOVED = "REM"


def get_color(agent):
    if agent.illness_state == SUSPECTIBLE:
        return "Green"
    elif agent.illness_state == INFECTED:
        return "Red"
    elif agent.illness_state == REMOVED:
        return "Gray"
    else:
        return "Yellow"


def boid_draw(agent):
    return {"Shape": "circle",
            "r": 2,
            "Filled": "true",
            "Color": get_color(agent)
            }


boid_canvas = SimpleCanvas(boid_draw, 500, 500)
model_params = {
    "population": 500,
    "width": 100,
    "height": 100,
    "speed": 5,
    "vision": 10,
    "separation": 2,
}

server = ModularServer(BoidFlockers, [boid_canvas], "Boids", model_params)
