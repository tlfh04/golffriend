from django.urls import path
from . import views

app_name = 'acc'
urlpatterns = [
    path('index/',views.index,name="index"),
    path('login/',views.ulogin,name="login"),
    path('logout/', views.ulogout, name="logout"),
    path('signup/', views.signup, name="signup"),
]