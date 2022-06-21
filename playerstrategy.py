# Created by M. Krouwel
from enum import Enum

class PlayerStrategy(Enum):
    RANDOM = 'RANDOM'
    MODEL = 'MODEL'
    AB = 'AB'
    MANUAL = 'MANUAL'