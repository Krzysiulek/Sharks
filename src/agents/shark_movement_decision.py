from enum import Enum


class SharkMovementDecision(Enum):
    MOVE_TO_FISH = "MOVE_TO_FISH"
    MOVE_TO_BLOOD = "MOVE_TO_BLOOD"
    MOVE_RANDOMLY = "MOVE_RANDOMLY"
    EAT_FISH = "EAT_FISH"
