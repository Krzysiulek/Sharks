from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule

from src.agents_factory import AgentsFactory
from .SimpleContinuousModule import SimpleCanvas
from .agents.fish_shoal_agent import FishShoalAgent
from .agents.pilot_fish_agent import PilotFishAgent
from .agents.shark_agent import SharkAgent
from .utils.drawer_utils import pilot_draw, shark_draw, shoal_draw


def draw_agent(agent):
    if type(agent) is FishShoalAgent:
        return shoal_draw(agent)
    elif type(agent) is SharkAgent:
        return shark_draw(agent)
    elif type(agent) is PilotFishAgent:
        return pilot_draw(agent)


model_params = {
    # shoal
    "shoal_population": UserSettableParameter("slider", "Ile ławic?", 4, 1, 100, 1),
    "shoal_speed": UserSettableParameter("slider", "Szybkość ławicy", 1, 1, 25, 1),
    "shoal_min_value": UserSettableParameter("slider", "Min. l. start. ryb w ławicy", 10, 1, 1000, 1),
    "shoal_max_value": UserSettableParameter("slider", "Max. l. start. ryb w ławicy", 100, 2, 1000, 1),
    # shark
    "sharks_population": UserSettableParameter("slider", "Ile rekinów?", 4, 1, 100, 1),
    "shark_speed": UserSettableParameter("slider", "Szybkość rekina i pilota", 2, 1, 25, 1),
    "shark_blood_vision": 200,
    "shark_fish_vision": 20,
    # pilot fish
    "pilot_vision": 50,
    "pilots_population": 40,
    # other
    "width": 100,
    "height": 100,
    "vision": 10,
    "separation": 2,
}

boid_canvas = SimpleCanvas(draw_agent, 500, 500)
fish_chart = ChartModule([{"Label": "Fish", "Color": "#00BFB2"}])
sharks_chart = ChartModule([{"Label": "Sharks", "Color": "#4D5C9E"}])
shoal_chart = ChartModule([{"Label": "Shoal", "Color": "#00BFB2"}])
pilots_chart = ChartModule([{"Label": "Pilots", "Color": "#d12802"}])

visualization_elements = [boid_canvas, fish_chart, sharks_chart, shoal_chart, pilots_chart]

server = ModularServer(model_cls=AgentsFactory,
                       visualization_elements=visualization_elements,
                       name="Sharks",
                       model_params=model_params)
