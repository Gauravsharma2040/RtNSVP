# geo/base.py
from abc import ABC, abstractmethod

class GeoResolver(ABC):
    @abstractmethod
    def resolve(self, event: dict) -> tuple[float, float]:
        pass
