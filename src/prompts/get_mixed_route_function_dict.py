function_dictionary = {
    "name": "consult_mix_routes_info",
    "description": "Specify the departure time and the mode of transportation to get the time, distance and carbon footprint for each possible option of the route.",
    "parameters": {
        "type": "object",
        "properties": {
            "departure_time": {
                "type": "string",
                "description": "The time of the departure in 'YYYY-MM-DD HH:MM:SS' format. Example: '2021-12-31 12:00:00'",
            },
            "routes": {
                "type": "array",
                "description": "The routes to consult",
                "items": {
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
                        "mode": {
                            "type": "string",
                            "description": "The mode of transportation. Example: 'driving'",
                            "enum": ["driving", "transit", "walking", "bicycling"],
                        },
                    },
                },
            },
        },
        "required": ["origin", "origin_region", "destination", "destination_region"],
    },
}
