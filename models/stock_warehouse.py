from odoo import models, fields, api
import requests

class WeatherDashboard(models.Model):
    _name = 'weather.dashboard'
    _description = 'Weather Dashboard'

    name = fields.Selection([
        ('Bangalore', 'Bangalore'),
        ('Mumbai', 'Mumbai'),
        ('Delhi', 'Delhi'),
        ('Chennai', 'Chennai'),
        ('Hyderabad', 'Hyderabad'),
        ('Pune', 'Pune'),
    ], string="City Name", default='Bangalore')
    weather_info = fields.Char(string="Weather Info", readonly=True)
    temperature = fields.Float(string="Temp", readonly=True)
    description = fields.Char(string="Sky", readonly=True)

    def fetch_weather(self):
        for record in self:
            api_key = "c132fb8ab7d5a8f085afc11239f49f2b"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={record.name}&appid={api_key}&units=metric"
            try:
                res = requests.get(url).json()
                if res.get('cod') == 200:
                    record.temperature = res['main']['temp']
                    record.description = res['weather'][0]['description'].capitalize()
                    record.weather_info = f"{record.temperature}°C - {record.description}"
                else:
                    record.weather_info = "City not found"
            except:
                record.weather_info = "Network Error"

    def clear_data(self):
        for record in self:
            record.temperature = 0
            record.description = False
            record.weather_info = False