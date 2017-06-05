from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^bot/', views.webhook, name='bot'),
    url(r'^foodcenter/', views.food_center_webhook, name= 'food'),
    # url(r'^relay/', vi)
]