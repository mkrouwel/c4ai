# Created by M. Krouwel
from typing import Any, List, Tuple

class Utils:

    @staticmethod
    def flatten(xss : List[List[Any]]) -> List[Any]:
        return [x for xs in xss for x in xs]

    @staticmethod
    def takeFirst(t : Tuple) -> Any:
        v, = t
        return v

    @staticmethod
    def takeSecond(t : Tuple) -> Any:
        _,v = t
        return v