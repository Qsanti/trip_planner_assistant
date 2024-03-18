# Create a singleton class called TravelPlan
import pandas as pd


class TravelPlan:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if not self.__initialized:
            self.__initialized = True
            self._travel_plan = []

    def add(self, route):
        self._travel_plan.append(route)

    def get_df(self):
        return pd.DataFrame(self._travel_plan)

    def clear(self):
        self._travel_plan = []
