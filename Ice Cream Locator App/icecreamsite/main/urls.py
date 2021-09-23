from django.urls import path
from . import views
app_name='main'
urlpatterns = [
    path('login', views.LoginView),
    path('signup', views.RegisterView),
    path('profile', views.ProfileView),
    path('map', views.MapView),
    path('store', views.StoreView),
    path('statistics',views.StatisticsView),
]