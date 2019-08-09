from django.urls import path, include
from . import views

urlpatterns = [

    # Game
    path('', views.start, name='start'),
    path('table/', views.play, name='play'),
    path('exit/', views.exit, name='exit'),

    # Decisions
    path('check/', views.check, name='check'),

    # Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]
