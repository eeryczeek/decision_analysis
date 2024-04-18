class Criterion:
    def __init__(self, v: float, p: float, q: float, value: float) -> None:
        self.v = v
        self.p = p
        self.q = q
        self.value = value


class BoundaryProfile:
    def __init__(self, criterions: dict[str, Criterion]) -> None:
        self.criterions = criterions

    def to_alternative(self) -> dict[str, float]:
        return {name: criterion.value for name, criterion in self.criterions.items()}
