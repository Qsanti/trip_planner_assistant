# Trip planner Assistant

Chat AI assistant to help trip planning. 🚗🚲🚆

### Main funtionalities

* Determine the **distance, duration and CO2 emissions on a given route from point A to point B**. Depending on whether you walk, pedal, use transportation or drive.
* It also d**etermines the total emission, distance and time for mixed routes**. Example: Walk from A to B and drive from B to C.
* It **stores the routes requested by the user in a Trip Planer table** that you can download as csv with its Gmaps links. Shows the total carbon emission.

### Example short use-case video

video.con (TODO)

### Instructions

1. **Clone respository**
2. **Buil the image**

   ```
   docker build -t trip-assistant .
   ```

3. **Run a Docker container**

   ```
   docker run -d --name trip-assistant -p 8000:8000 trip-assistant
   ```

4. **Go to app**
   Exposed in `localhost:8000`.
5. **Set api keys:**

   * OpenAi api key.

     * Get it from here [API keys - OpenAI API](https://platform.openai.com/api-keys)
   * Google Maps Api key.

     * Create GCP proyect.
     * Go to the Google Maps Platform > Credentials page. Go to the Credentials page.
     * On the Credentials page, click Create credentials > API key. The API key created dialog displays your newly created API key.
     * Click Close. The new API key is listed on the Credentials page under API keys.
     * Enable [Address Validation API – Marketplace – RouteAPI – Google Cloud console](https://console.cloud.google.com/marketplace/product/google/addressvalidation.googleapis.com?q=search&referrer=search&authuser=1&project=routeapi-417104) for your proyect.
6. **Start trying it!**

## General comments

The main idea of this development, given the instructions and the time limitation (~4 hours). It was about creating a functional AI chat prototype.

The **following objectives were effectively achieved**:

* Implement a Chatbot using an assistant LLM service.
* A Simple Open source and easy to deploy & share chat interface.
* Integrate Google Gmaps API to get routes between points.
* Get the maps URL to share routes.
* Create a downloadable travel calendar.
* Integrate tools to the LLM to develop an AI Agent capable of:
  * Correct route API call to collect information about times, duration and emission of the different travel modes, and their Maps url.
  * Correctly update the travel plan objet to save the routes the user ask (including date time and gmaps url)
  * Calculate total time and emissions using mixed routes. Ex: walk from A to B and drive from B to C.
* Modularize the project to facilitate prompt engineering for easy iteration.
* Modularize Agent chat logic to easily add, remove, or modify tools the agent can use.

The **objectives that were left in the middle** (due time constrain) of the development were:

* Integrate a Map inside the app. This was partially achived (but was removed/commented in the final version) but the part of displaying the routes was missing.
* Give the agent more freedom to interact with the Travel Plan. Currently you can only "push" information, but the idea was to give you a `pandas` tool with good contrains to perform stats add/remove/modify routes. Also this tool was removed from the final version. You can see [Guada my free to use Data Analyst](https://www.youtube.com/watch?v=LwgiALJGBBM) who helps LATAM people to manipulate datasets and sheets, by plotting and applying statistics tachniques.
* Support Audio messages. I had the Whisper integration but, didn't have time to figure out how to add voice notes to streamlit chat.
* Add flights routes. Since the google flights api is disabled I had to research for other Apis to get these information, but I decided not to integrate them at the end so as not to add one more api key and because I needed time to integrate it into the flow.

**Goals that I had in mind** but haven't been able to face them (yet)

* Make Tools more flexible. As in all AI chat I've implemented, first I start with "hard" tools and a "wide" system message. But once you validate the proyect is working (and you gather inspiration and ideas from the prototype you're testing) I start to refine the tools and prompting. My main Ideas were to let the agent make calculations and give them "optimization tools" so It can answer an perform more complex tasks.
* Add a RAG tool with environmental information so the agent can resolve operational questions. This information "search" tool technique is very useful to avoid hallucination in my experience and to limit the scope of the AI.
* Add a more classic algorithm to complement. Take advantage of the Distance Matrix APIs and some emissions APIs to create a good emissions Matrix and use Dijkstra's algorithm to find the best paths.

## Code Overview

This proyect is structured in the following way:

```
trip_planner_assistant/
│
├── src/                         # Main directory of the Python application.
│   ├── ai.py                  # Entry point for the AI module.
│   ├── llm_utils/
│   │   └── run_llm.py      # Generic function to run LLM AGen with a prompt, llm model, chat history and tools
│   ├── prompts/                 # LLM prompts for system and tools.
│   │   ├── tripy_system.py                               # LLM prompt for system.
│   │   ├── add_route_funtion_dict.py              # Function dict for tools.
│   │   ├── get_route_info_function_dict.py
│   │   └── get_mixed_route_function_dict.py
│   ├─  functions/                 # Functions to be called by the LLM
│   │   └── functions.py       # The three functions (add_route, get_route_info, get_mixed_route) defined here
│   ├── utils/                 # Utility functions for the AI module.
│   │   ├── gmapsutils.py               # Google Maps API utility functions.
│   │   └── parsers.py                      # Utility functions for parsing and formatting data.
│   └── structures/                 # Main classes and structures for the application.
│       └── travelplan.py         # TravelPlan singleton class. Modified by the AI module and rendered Streamlit app.
│
├── app.py                # Main entry point of the Streamlit application.
│
├── .streamlit                   # Streamlit configuration directory.
│
├── Dockerfile                    # Instructions to containerize the application.
│
├── requirements.txt              # List of dependencies required for the application.
│
├── .gitignore                    # Lists excluded files/directories.
│
└── README.md                     # Detailed project documentation.
```

### Code logic

The project is organized in the following way:

* The `app.py` file is the main entry point of the Streamlit application. It is responsible for rendering the user interface and handling user inputs via the chat interface.. It interacts with the `travelplan` singleton class to display the current state of the travel plan lead the user donwload it. Also ask the api keys and export them to the environment variables.
* When a response need to be generated, the `generate_response` function from `ai.py` is called. And here is where all the magic happens.
* The `ai.py` file is the entry point for the AI module. It prepares all of the components required to run the LLM model:

* Initialize the LLM model.
* Loads the system prompt and tools prompts dictionaries.
* Loads the functions to be called by the LLM and creates a `toolbox`, wrapping the functions with their corresponding prompts dictionaries.
* Import the `run_llm` function from `llm_utils` that is a generic function to run LLM AGen with a prompt, llm model, chat history and tools. (imported in the previous steps)

* So when the `generate_response` function is called, it uses the `run_llm` function, to run the LLM model with the system prompt, chat history and tools to generate a response. The response is then returned to the `app.py` file to be displayed to the user.
* The functions to be called by the LLM are defined in the `functions.py` file and (as said before) are wrapped with their corresponding prompts dictionaries in the `toolbox` object. These functions are triggered by the LLM model when the user asks for a specific action to be performed or when the LLM model needs to gather information to generate a response. These are:

  -`get_route_info`: Gets information about a specific route. Given the the start and end locations, among other parameters, it does the following:

  1. Validates the input parameters, using the adress validation api.
  2. Gets the route information from the Google Maps API for each available mode of transportation (driving, walking, bicycling, and transit).
  3. Get and format the total time and distance for each mode of transportation. And calculates an estimated CO2 emissions.
  4. Generate the Maps URL for each mode of transportation.

  -`get_mixed_route`: Gets a mixed route. Given the a list of legs, each with a start and end location, and a mode of transportation, it does the following:

  1. Validates the input parameters, using the adress validation api.
  2. Gets the route information from the Google Maps API for each leg with the specified mode of transportation.
  3. Calculates an estimated CO2 emissions and the total time and distance for the entire route.
  4. Generate the Maps URL for each leg and mode of transportation.

  -`add_route`: Adds a route to the travel plan. Given all the parameters, it adds a new route to the travel plan and returns a confirmation message. This functions initializes the `travelplan` singleton class and calls the `add_route` method to add the route to the travel plan. So the display is updated with the new route (cause is using th same instance of the `travelplan`).
