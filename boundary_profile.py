class BoundaryProfile:
    def __init__(self, criterions: dict[str, dict[str, int]]) -> None:
        """
        example of criterion:
        {
            "criterion1": {
                "v": 0.5,
                "p": 0.2,
                "q": 0.1,
                "value": 7,
            }
        }
        """
        self.criterions = criterions
