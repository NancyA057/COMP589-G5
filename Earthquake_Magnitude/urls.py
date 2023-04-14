from django.urls import path
from app import views
from app import magnitude

urlpatterns = [
    path('', views.landing, name='landing'),
    path('city/', views.city_view, name='city_view'),
    path('magnitude/', views.get_magnitude, name='get_magnitude'),
    path('my_view/', views.my_view, name='my_view'),
    # path('earthquake_magnitude/', magnitude.MLClassifier(), name='MLClassifier'),
]
