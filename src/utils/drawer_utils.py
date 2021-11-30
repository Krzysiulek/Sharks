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
    return draw_circle(r=1, color="#b202d1")

def blood_draw(agent):
    color = "#d12802"
    max_radius = agent.max_blood_radius + 1
    xd = int((max_radius - agent.radius) / max_radius * 255)
    xd = max(16, xd)

    opacity = str(hex(xd)[2:])
    print(str(hex(xd)) + " : " + opacity + " : " + str(xd))
    return draw_circle(r=agent.radius, color=str(color + opacity))