# Created by M. Krouwel

from typing import Any, List, Tuple

class Utils:

    @staticmethod
    def flatten(xss : List[List[Any]]) -> List[Any]:
        return [x for xs in xss for x in xs]

    @staticmethod
    def filterEqual(xs : List[Any], c : Any) -> Any:
        return [v for v in xs if v == c]

    @staticmethod
    def takeFirst(t : Tuple) -> Any:
        return t[0]

    @staticmethod
    def takeSecond(t : Tuple) -> Any:
        return t[1]