from src.utils.fish_shoal_utils import get_fish_r


def draw_circle(r, color):
    return {
        "Shape": "circle",
        "r": r,
        "Filled": "true",
        "Color": color
    }


def shoal_draw(agent):
    return draw_circle(r=get_fish_r(agent.fish_amount),
                       color="#00BFB2")


def shark_draw(agent):
    return draw_circle(r=3, color="#4D5C9E")


def pilot_draw(agent):
    return draw_circle(r=1, color="#d12802")