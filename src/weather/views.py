import requests
# import json
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import City
from .forms import CityForm


def index(request):
    url = 'https://samples.openweathermap.org/data/2.5/find?q={}&units=metric&appid=b6907d289e10d714a6e88b30761fae22'
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
        return HttpResponseRedirect(request.path_info)

    form = CityForm()

    cities = City.objects.all()
    weather_data = []
    for city in cities:
        result = requests.get(url.format(city)).json()
        # print(json.dumps(result, indent=4))
        city_weather = {
            'city': city.name,
            'temprature': result['list'][0]['main']['temp'],
            'description': result['list'][0]['weather'][1]['description'],
            'icon': result['list'][0]['weather'][1]['icon']
        }
        weather_data.append(city_weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)
