from django.urls import path, include
from . import views

urlpatterns = [

    # Game
    path('', views.start, name='start'),
    path('table/', views.play, name='play'),

    # Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]
