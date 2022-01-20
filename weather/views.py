from django.shortcuts import render
from os import getenv
from requests import get
from .models import City
from .forms import CityForm

def index(request):
    URL = getenv('API_URL')
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_weather = get(URL.format(form.cleaned_data['name'])).json()
            if city_weather['cod'] == 200:
                weather = {
                    'city': city_weather['name'],
                    'temperature': city_weather['main']['temp'],
                    'description': city_weather['weather'][0]['description'],
                    'icon': city_weather['weather'][0]['icon']
                }
                context = {'weather': weather, 'form':form}
            else:
                context = {'form':form, 'error':'This city not found'}

    else:
        form = CityForm()
        weather_data = []
        cities = City.objects.all()
        for city in cities:
            city_weather = get(URL.format(city)).json()
            weather = {
                'city': city,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }

            weather_data.append(weather)

        context = {'weather_data' : weather_data, 'form':form}
    return render(request, 'weather/index.html', context=context)
