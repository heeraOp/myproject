from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = "index"),
    path('download/',views.download, name = "download"),
    path('counter', views.counter, name ="counter"),
    path('register',views.register, name = "register"),
    path('login',views.login, name = "login")

]