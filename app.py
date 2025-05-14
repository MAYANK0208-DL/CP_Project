from flask import Flask, render_template, request, url_for
import requests
from datetime import datetime
import pytz

app = Flask(__name__)
API_KEY = "9fc7a7a2964c1df2075fcad2c3bff67b"

WEATHER_BG_MAP = {
    "clear": "clear.jpeg",
    "rain": "rain.mp4",
    "cloud": "cloud.gif",
    "snow": "snow.gif",
    "thunder": "thunder.mp4"
}

def get_background(description):
    desc = description.lower()
    for key in WEATHER_BG_MAP:
        if key in desc:
            return url_for('static', filename=f'background/{WEATHER_BG_MAP[key]}')
    return url_for('static', filename='background/default.gif')

def get_weather_emoji(description):
    desc = description.lower()
    if 'clear' in desc:
        return '☀️'
    elif 'cloud' in desc:
        return '☁️'
    elif 'rain' in desc:
        return '🌧️'
    elif 'thunder' in desc:
        return '⛈️'
    elif 'snow' in desc:
        return '❄️'
    else:
        return '🌈'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    forecast = None
    background_url = url_for('static', filename='background/default.gif')

    if request.method == 'POST':
        city = request.form['city'].strip()
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(weather_url)
        forecast_response = requests.get(forecast_url)

        if response.status_code == 200 and forecast_response.status_code == 200:
            data = response.json()
            forecast_data = forecast_response.json()
            description = data['weather'][0]['description']
            timezone = pytz.timezone("Asia/Kolkata")
            sunrise = datetime.fromtimestamp(data['sys']['sunrise'], timezone).strftime('%I:%M %p')
            sunset = datetime.fromtimestamp(data['sys']['sunset'], timezone).strftime('%I:%M %p')

            weather = {
                'city': data['name'],
                'temperature': round(data['main']['temp']),
                'description': description,
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed'],
                'time': datetime.now(timezone).strftime("%A, %d %B %Y %I:%M %p"),
                'sunrise': sunrise,
                'sunset': sunset,
                'emoji': get_weather_emoji(description)
            }

            forecast = []
            for i in range(0, 40, 8):
                item = forecast_data['list'][i]
                forecast.append({
                    'date': datetime.fromtimestamp(item['dt']).strftime('%A'),
                    'temp': round(item['main']['temp']),
                    'icon': item['weather'][0]['icon'],
                    'desc': item['weather'][0]['description'].title()
                })

            background_url = get_background(description)
        else:
            weather = {'error': 'City not found or network issue.'}

    return render_template('index.html', weather=weather, background_url=background_url, forecast=forecast)

if __name__ == '__main__':
    app.run(debug=True)
