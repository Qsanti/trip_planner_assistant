# Description: This file contains the functions to interact with the Google Maps API

import googlemaps
from datetime import datetime
import urllib.parse
import os

from ..utils.parsers import parse_distance_to_km, parse_time_to_mins


GMAPS_API_KEY = os.environ.get("GMAPS_API_KEY")

gmaps = googlemaps.Client(key=GMAPS_API_KEY)
g_per_km = {"transit": 10, "driving": 50, "air": 100, "walking": 0, "bicycling": 0}


# Function to get the possible routes info.
def get_routes(
    A: str,
    B: str,
    mode: str,
    alternatives: bool,
    waypoints: list,
    optimize_waypoints: bool,
    traffic_model: str,
    departure_time: datetime,
):
    directions_result = gmaps.directions(
        A,
        B,
        mode=mode,
        alternatives=alternatives,
        waypoints=waypoints,
        optimize_waypoints=optimize_waypoints,
        traffic_model=traffic_model,
        departure_time=departure_time,
    )
    return directions_result


# Function to get the insight for a route.
def get_insight_for_route(route: dict):
    time = route["legs"][0]["duration"]["text"]
    distance = route["legs"][0]["distance"]["text"]
    carbon = 0
    DISTANTCE = 0
    for step in route["legs"][0]["steps"]:
        step_distance = parse_distance_to_km(step_distance)
        carbon += step_distance * g_per_km[step["travel_mode"].lower()]

    return {"time": time, "distance": distance, "carbon": carbon}


# Function to get the valid address.
def get_valid_address(address: str, regionCode: str):
    addressvalidation_result = gmaps.addressvalidation([address], regionCode=regionCode)
    return addressvalidation_result["result"]["address"]["formattedAddress"]


# Function to create a maps URL
def create_maps_url(
    origin=None,
    destination=None,
    origin_place_id=None,
    destination_place_id=None,
    travelmode=None,
    dir_action=None,
    waypoints=None,
):
    base_url = "https://www.google.com/maps/dir/?api=1"
    params = {}

    origin_encoded = urllib.parse.quote(origin)
    destination_encoded = urllib.parse.quote(destination)

    if origin:
        params["origin"] = origin
    if destination:
        params["destination"] = destination
    if origin_place_id:
        params["origin_place_id"] = origin_place_id
    if destination_place_id:
        params["destination_place_id"] = destination_place_id
    if travelmode and travelmode in ["driving", "walking", "bicycling", "transit"]:
        params["travelmode"] = travelmode
    if dir_action and dir_action == "navigate":
        params["dir_action"] = dir_action
    if waypoints:
        params["waypoints"] = waypoints

    # Construct the query string
    query_string = urllib.parse.urlencode(params, safe=",|").replace("%7C", "|")
    return f"{base_url}&{query_string}"
