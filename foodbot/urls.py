from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^bot/', views.webhook, name='bot'),
    # url(r'^foodcenter/', )
]