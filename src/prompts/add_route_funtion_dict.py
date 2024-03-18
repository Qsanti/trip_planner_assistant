function_dictionary = {
    "name": "add_route_to_travel_plan",
    "description": "Search for posible routes from A to B. The function will return the time, distance and carbon footprint for each possible option of the route",
    "parameters": {
        "type": "object",
        "properties": {
            "origin": {
                "type": "string",
                "description": "The starting point of the route. Example: 'New York, NY'",
            },
            "destination": {
                "type": "string",
                "description": "The destination point of the route. Example: 'Newark, NJ'",
            },
            "departure_time": {
                "type": "string",
                "description": "The time of the departure in ISO 8601 format. Example: '2021-12-31T12:00:00'",
            },
            "mode": {
                "type": "string",
                "description": "The mode of transportation. Example: 'driving'",
                "enum": ["driving", "transit", "walking", "bicycling"],
            },
            "waypoints": {
                "type": "array",
                "description": "The waypoints of the route. Example: ['Newark, NJ', 'New York, NY']",
                "items": {
                    "type": "string",
                },
            },
        },
        "required": ["origin", "destination", "departure_time", "mode"],
    },
}
