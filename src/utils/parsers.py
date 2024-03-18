def parse_time_to_mins(time: str) -> float:
    "get time in format x days y hours z minutes w seconds and return the total time in hours"
    time = time.split(" ")
    total_time = 0
    if "days" in time:
        day_index = time.index("days")
        total_time += int(time[day_index - 1]) * 24 * 60
    if "hours" in time:
        hour_index = time.index("hours")
        total_time += int(time[hour_index - 1]) * 60
    if "minutes" in time:
        minute_index = time.index("minutes")
        total_time += int(time[minute_index - 1])
    if "seconds" in time:
        second_index = time.index("seconds")
        total_time += int(time[second_index - 1]) / 60

    return total_time


def parse_distance_to_km(distance: str) -> float:
    "get distance in format x km and return the distance in km"
    distance, unit = distance.split(" ")
    distance = float(distance)
    if unit == "m":
        distance = distance / 1000

    if unit == "ft":
        distance = distance * 0.0003048

    if unit == "mi":
        distance = distance * 1.60934
    return distance
