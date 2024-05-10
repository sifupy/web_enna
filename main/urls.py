from django.urls import path
from .views import *  

urlpatterns = [
    path('login/', login_view, name='login'),  
    path('logout/', logout_view, name='logout'),  
    path('',home_view,name="home"),
    path('employes/',page_acc,name="employes"),
    path('page_admin/',admin_view,name="page_admin"),
    path('ats/<matricule>',ats_view,name="ats"),
    path('profile/<matricule>',profile_view,name="profile"),
    path('attestation/<matricule>',attestation_view,name="attestation"),
    path('suprimmer_user/<matricule>',suprimmer_view,name="suprimmer_user"),
    path('contact_us/',contact_view,name="contact_us"),
]