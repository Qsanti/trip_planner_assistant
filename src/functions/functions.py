from ..utils.gmapsutils import (
    get_insight_for_route,
    get_routes,
    get_valid_address,
    create_maps_url,
)
from ..structures.travelplan import TravelPlan
from ..utils.parsers import parse_distance_to_km, parse_time_to_mins

from datetime import datetime


def get_posible_routes_info(
    origin: str,
    origin_region: str,
    destination: str,
    destination_region: str,
    waypoints: list = [],
    departure_time: str = None,
):
    origin = get_valid_address(origin, origin_region)
    destination = get_valid_address(destination, destination_region)
    waypoints = [get_valid_address(waypoint, origin_region) for waypoint in waypoints]

    mode_insigths = {}

    if departure_time is None:
        departure_time = datetime.now()
    else:
        departure_time = datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%S")

    for mode in ["driving", "transit", "walking", "bicycling"]:
        routes = get_routes(
            A=origin,
            B=destination,
            mode=mode,
            departure_time=departure_time,
            traffic_model=None,
            alternatives=False,
            optimize_waypoints=False,
            waypoints=waypoints,
        )
        mode_insigths[mode] = []
        for route in routes:
            insight = get_insight_for_route(route)
            print(
                f"Mode: {mode}, Time: {insight['time']}, Distance: {insight['distance']}, Carbon: {insight['carbon']}"
            )
            mode_insigths[mode].append(insight)

        # # for each mode get just the less distance route
        # mode_insigths[mode] = sorted(
        #     mode_insigths[mode], key=lambda x: x["distance"], reverse=False
        # )[0]

    str_info = f"Routes from {origin} to {destination}:\n"

    for mode, insight in mode_insigths.items():
        str_info += f"\n{mode}:\n"
        for i, route in enumerate(insight):
            str_info += f"Route {i+1}:\n"
            str_info += f"Time: {route['time']}\n"
            str_info += f"Distance: {route['distance']}\n"
            str_info += f"Carbon: {route['carbon']}\n"
            str_info += f"URL: {create_maps_url(origin=origin, destination=destination, travelmode=mode)}\n"

    return str_info


def add_route_to_travel_plan(
    origin: str, destination: str, departure_time: str, mode: str, waypoints: list = []
):
    # get datetime from ISO 8601 format
    departure_time = datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%S")

    travel_plan = TravelPlan()
    url = create_maps_url(origin=origin, destination=destination, travelmode=mode)
    insight = get_insight_for_route(
        get_routes(
            A=origin,
            B=destination,
            mode=mode,
            departure_time=departure_time,
            traffic_model=None,
            alternatives=False,
            optimize_waypoints=False,
            waypoints=waypoints,
        )[0]
    )

    travel_plan.add(
        {
            "Day": departure_time.strftime("%Y-%m-%d"),
            "Hour": departure_time.strftime("%H:%M:%S"),
            "Origin": origin,
            "Destination": destination,
            "Travel Mode": mode,
            "GmapsURL": url,
            "Time": insight["time"],
            "Distance": insight["distance"],
            "Carbon": insight["carbon"],
        }
    )

    return f"Route added to travel plan!: Give this confrimation info \nOrigin: {origin}\nDestination: {destination}\nDeparture Time: {departure_time}\nMode: {mode}\nURL: {url}"


def get_mixed_routes_info(departure_time: str, routes: list):

    mode_insigths = {}

    if departure_time is None:
        departure_time = datetime.now()
    else:
        departure_time = datetime.strptime(departure_time, "%Y-%m-%d %H:%M:%S")

    insights = []

    for route in routes:
        origin = get_valid_address(route["origin"], route["origin_region"])
        destination = get_valid_address(
            route["destination"], route["destination_region"]
        )
        mode = route["mode"]
        routes = get_routes(
            A=origin,
            B=destination,
            mode=mode,
            departure_time=departure_time,
            traffic_model=None,
            alternatives=False,
            optimize_waypoints=False,
            waypoints=[],
        )

        for route in routes:
            insight = get_insight_for_route(route)
            insights.append(insight)

    str_info = f"Mix route from {origin} to {destination}:\n"
    total_time = 0
    total_distance = 0
    total_carbon = 0
    for insight in insights:
        str_info += f"Time: {insight['time']}\n"
        str_info += f"Distance: {insight['distance']}\n"
        str_info += f"Carbon: {insight['carbon']}\n"
        str_info += f"URL: {create_maps_url(origin=origin, destination=destination, travelmode=mode)}\n"
        total_time += parse_time_to_mins(insight["time"])
        total_distance += parse_distance_to_km(insight["distance"])
        total_carbon += insight["carbon"]

    str_info += f"Total Time: {total_time}\n"
    str_info += f"Total Distance: {total_distance}\n"
    str_info += f"Total Carbon: {total_carbon}\n"

    return str_info
