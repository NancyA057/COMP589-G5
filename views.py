from django.shortcuts import render
import googlemaps
from django import forms

from django.shortcuts import render
import datetime
from app import mymodule
from app import magnitude


GOOGLE_MAPS_API_KEY = 'AIzaSyApp6dlCxvAF4Q197JGAvqgnZj5TjUxHZQ'

class CityForm(forms.Form):
    city = forms.CharField(label='City', max_length=100)
    date_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

def get_lat_lng(city):
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    geocode_result = gmaps.geocode(city)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return {'lat': lat, 'lng': lng}

def landing(request):
    return render(request, 'earthquake_magnitude/landing.html')

def get_magnitude(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
    return render(request, 'earthquake_magnitude/magnitude.html')

def city_view(request):
    form = CityForm()
    city = None
    lat_lng = None
    date_time = None
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data.get('city')
            date_time = form.cleaned_data['date_time']
            lat_lng = get_lat_lng(city)
    context = {
        'form': form,
        'city': city,
        'lat_lng': lat_lng,
        'date_time': date_time
    }
    return( render(request, 'earthquake_magnitude/index.html', context))


def my_view(request):
    if request.method == 'POST':
        # Get the parameters from the form
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        datetime_string = request.POST.get('datetime')
        if datetime_string is not None:
        # Convert the date string to a datetime object
            datetime_obj = datetime.datetime.strptime(datetime_string, '%Y-%m-%dT%H:%M:%S')
        
            # Get the date and time strings from the datetime object
            date_string = datetime_obj.strftime('%m/%d/%Y')
            time_string = datetime_obj.strftime('%H:%M:%S')
        
            # Call the Python function in the other file
            #result = mymodule.my_function(param1, param2, date_string, time_string)
            result = magnitude.MLClassifier(date_string, time_string, latitude, longitude)
        
            # Format the result as a string
            #result_string = f"{result}"
        
        
            # Render the HTML template with the result
            return render(request, 'earthquake_magnitude/magnitude.html', {'result': result})
        else:
            
            return render(request, 'earthquake_magnitude/magnitude.html', {'error': 'Datetime field is required.'})

    else:
        # Set the initial value of the datetime field
        initial_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return render(request, 'earthquake_magnitude/magnitude.html', {'initial_datetime': initial_datetime})


