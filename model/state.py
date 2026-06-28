from dataclasses import dataclass
import math

@dataclass
class State:
    id: str
    Name: str
    Capital: str
    Lat: float
    Lng: float
    Area: int
    Population: int
    Neighbors: str
    numSightings: int = 0

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.id

    def distance(self, other):
        R = 6371
        dlat = math.radians(other.Lat - self.Lat)
        dlon = math.radians(other.Lng - self.Lng)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(self.Lat)) * math.cos(math.radians(other.Lat)) * math.sin(
            dlon / 2) ** 2
        return R * 2 * math.asin(math.sqrt(a))