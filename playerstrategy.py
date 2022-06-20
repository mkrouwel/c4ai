# Created by M. Krouwel
from enum import Enum
from abc import ABC, abstractmethod


from typing import List, Tuple, Any

class PlayerStrategy(Enum):
    RANDOM = 'RANDOM'
    MODEL = 'MODEL'
    AB = 'AB'
    MANUAL = 'MANUAL'