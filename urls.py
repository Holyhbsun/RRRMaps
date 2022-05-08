from django.urls import include, path
from django.contrib import admin
import view

urlpatterns = [
    path('index/', view.index),
    path('solve/', view.solve),
]