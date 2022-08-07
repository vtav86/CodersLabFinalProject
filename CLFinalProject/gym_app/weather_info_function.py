import requests

conditions = {
    'Thunderstorm': '⛈',
    'Clouds': '☁',
    'Drizzle': '🌧️',
    'Rain': '🌧️',
    'Snow': '❄',
    'Mist': '🌫️',
    'Smoke': '🌫️',
    'Haze': '🌫️',
    'Dust': '🌫️',
    'Fog': '🌫️',
    'Sand': '🌫️',
    'Ash': '🌫️',
    'Squall': '🌬️',
    'Tornado': '🌪️',
    'Clear': '☀️',
    'Not found': 'A good day to climb!️',

}


def get_weather():
    # Do not embed api key
    # call to environment variable import os os.getenv
    # .env files dotenv module
    api_key = "563e77eb1aa4156bb5dcab597d8e1abd"
    weather_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "Yerevan"
    complete_url = weather_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        main_info = x['main']
        current_temperature = main_info["temp"]
        description = x["weather"]
        weather_description = description[0]["main"]
        try:
            weather_image = conditions[weather_description]
        except KeyError:
            weather_image = conditions['Not found']
        weather_statement = "Currently " + str(
            current_temperature) + "°C in Yerevan and " + weather_description.lower() + ' ' + weather_image
        return weather_statement
    else:
        weather_statement = "It's a great day to climb!"
        return weather_statement
