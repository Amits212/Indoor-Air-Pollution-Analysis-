from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class People(BaseModel):
    name: Optional[str]
    age: Optional[int]
    is_smoking: bool = False

class Floor(BaseModel):
    number: Optional[int]
    peoples: Optional[List[People]]

class PollutionEvent(BaseModel):
    event: str
    pollution: float

class Building(BaseModel):
    name: str
    floors: Optional[List[Floor]] = []
    pollution_percentage: float = 0
    analysis: Dict[str, PollutionEvent] = {}

    def calculate_pollution(self):
        for floor in self.floors:
            for person in floor.peoples:
                if person.is_smoking:
                    self.pollution_percentage += 1

    def make_analysis(self, time: str, event: str):
        self.analysis[time] = PollutionEvent(event=event, pollution=self.pollution_percentage)
