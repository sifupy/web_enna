from django.urls import path
from .views import *  

urlpatterns = [
    path('login/', login_view, name='login'),  
    path('home/',home_view,name="home"),
    path('employes/',page_acc,name="employes"),
    path('page_admin/',admin_view,name="page_admin"),
    path('contact_us/',contact_view,name="contact_us"),
]