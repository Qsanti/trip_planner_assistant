# Trip planner Assistant

Chat AI assistant to help trip planning. 🚗🚲🚆

### Main funtionalities

* Determine the **distance, duration and CO2 emissions on a given route from point A to point B**. Depending on whether you walk, pedal, use transportation or drive.
* It also d**etermines the total emission, distance and time for mixed routes**. Example: Walk from A to B and drive from B to C.
* It **stores the routes requested by the user in a Trip Planer table** that you can download as csv with its Gmaps links. Shows the total carbon emission.

### Example short use-case video

### Instructions

1. **Clone respository**
3. **Buil the image**

   ```
   docker build -t trip-assistant .
   ```

4. **Run a Docker container**

   ```
   docker run -d --name trip-assistant -p 8000:8000 trip-assistant
   ```

5. **Go to app**
   Exposed in `localhost:8000`.
6. **Set api keys:**
   * OpenAi api key.

     * Get it from here [API keys - OpenAI API](https://platform.openai.com/api-keys)
   * Google Maps Api key.

     * Create GCP proyect.
     * Go to the Google Maps Platform > Credentials page. Go to the Credentials page.
     * On the Credentials page, click Create credentials > API key. The API key created dialog displays your newly created API key.
     * Click Close. The new API key is listed on the Credentials page under API keys.
     * Enable [Address Validation API – Marketplace – RouteAPI – Google Cloud console](https://console.cloud.google.com/marketplace/product/google/addressvalidation.googleapis.com?q=search&referrer=search&authuser=1&project=routeapi-417104) for your proyect.
7. **Start trying it!**

## General comments
