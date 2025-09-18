from django.shortcuts import render
from django.contrib import messages
import requests
import datetime



# Create your views here.

def home(request):
    if 'city' in request.POST:
        city=request.POST['city']
    else:
        city='jabalpur'
    
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=a2a60e5a5258fd801a9cc17d23d3cf18"
    weather_params = {"units":"metric"}

    # API_KEY = 'AIzaSyB43IqUCRSssNrp0wSt2P9ecjYVdz362f0'
    # SEARCH_ENGINE_ID = 

    # query = city + "1920x1080"
    # page = 1
    # start = (page-1)*10 + 1
    # searchType = 'image'
    # city_url = f'https://www.googleapis.com/customsearch/v1"f"?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}""&q={city}&searchType=image&num='

    # data = requests.get(city_url).json()
    # count = 1
    # search_items = data.get("items") 
    # image_url =search_items[1]['link']


    GOOGLE_API_KEY = "AIzaSyB43IqUCRSssNrp0wSt2P9ecjYVdz362f0"
    SEARCH_ENGINE_ID = "e01b7d64444bb4fa5"
    search_url = (
        "https://www.googleapis.com/customsearch/v1"
        f"?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
        f"&q={city}+cityscape&searchType=image&num=1"
    )

    try:
        data = requests.get(weather_url,weather_params).json()

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        image_resp = requests.get(search_url).json()
        items = image_resp.get("items", [])
        image_url = items[0]["link"] if items else ""   # fallback to a default if empty

        return render(request, "weatherapp/index.html", {
            'description': description, 
            'icon': icon, 
            'temperature':temp, 
            'day': day,
            'city':city,
            'exception_occured': False,
            'image_url' : image_url
            })
    except:
        exception_occured = True
        messages.error(request, 'entered data is not available')
        day=datetime.date.today()
        return render(request, "weatherapp/index.html", {
            'description': 'clear sky', 
            'icon':'01d', 
            'temperature':25, 
            'day': day,
            'city':'Jabalpur',
            'exception_occured': True})
    



    