from typing import Any, List

class Utils:

    def flatten(xss : List[List[Any]]) -> List[Any]:
        return [x for xs in xss for x in xs]