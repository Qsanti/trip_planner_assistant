import pandas as pd


# Singleton class to store the travel plan.
# This class is used to store the travel plan in a singleton way, so the travel plan can be accessed from any part of the code.
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
        "Add a route to the travel plan"
        self._travel_plan.append(route)

    def get_df(self):
        "Return the travel plan as a DataFrame"
        return pd.DataFrame(self._travel_plan)

    def clear(self):
        "Clear the travel plan"
        self._travel_plan = []
