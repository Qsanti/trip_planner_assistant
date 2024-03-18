function_dictionary = {
    "name": "consult_route_info",
    "description": "Search for posible routes from A to B. The function will return the time, distance and carbon footprint for each possible option of the route",
    "parameters": {
        "type": "object",
        "properties": {
            "origin": {
                "type": "string",
                "description": "The starting point of the route. Example: 'New York, NY'",
            },
            "origin_region": {
                "type": "string",
                "description": "The region of the starting point of the route. Example: 'US'",
            },
            "destination": {
                "type": "string",
                "description": "The destination point of the route. Example: 'Newark, NJ'",
            },
            "destination_region": {
                "type": "string",
                "description": "The region of the destination point of the route. Example: 'US'",
            },
            "departure_time": {
                "type": "string",
                "description": "The time of the departure in 'YYYY-MM-DDTHH:MM:SS' format. Example: '2021-12-31T23:59:59'",
            },
            # "waypoints": {
            #     "type": "array",
            #     "description": "The waypoints of the route. Example: ['Newark, NJ', 'New York, NY']",
            #     "items": {
            #         "type": "string",
            #     },
            # },
        },
        "required": ["origin", "origin_region", "destination", "destination_region"],
    },
}
