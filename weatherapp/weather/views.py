from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

MAX_ON_PAGE = 5


def index(request):
    appid = '544fc8912150f202a47c1e3d09ecfc7c'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&lang=ru&units=metric&appid=' + appid
    url_1 = 'https://api.openweathermap.org/data/2.5/weather?q={}&lang=ru&appid=' + appid
    error_message = ''
    message = ''
    message_1 = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                res = requests.get(url.format(new_city)).json()
                res_1 = requests.get(url_1.format(new_city)).json()

                if res['cod'] == 200 or res_1['cod'] == 200:
                    form.save()
                else:
                    error_message = 'Ошибка! Города не существует!'
            else:
                error_message = 'Ошибка! Город уже в списке!'

        if error_message:
            message = error_message
            message_1 = 'is-danger'
        else:
            message = 'Город успешно добавлен в список'
            message_1 = 'is-succes'

    print(error_message)
    form = CityForm()

    cities = City.objects.order_by('-id')[:MAX_ON_PAGE]
    all_cities = []

    for city in cities:
        res = requests.get(url.format(city)).json()
        res_1 = requests.get(url_1.format(city)).json()
        city_info = {
            'city': city.name,
            'temp': res["main"]["temp"],
            'description': res_1["weather"][0]["description"],
            'wind': res_1["wind"]["speed"],
            'icon': res_1["weather"][0]["icon"]
        }

        all_cities.append(city_info)

    context = {
        'all_info': all_cities,
        'form': form,
        'message': message,
        'message_1': message_1
    }
    return render(request, 'weather/index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')
