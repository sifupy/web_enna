from django.urls import path
from .views import *  

urlpatterns = [
    path('login/', login_view, name='login'),  
    path('logout/', logout_view, name='logout'),  
    path('',home_view,name="home"),
    path('employes/',page_acc,name="employes"),
    path('page_admin/',admin_view,name="page_admin"),
    path('relve_emo/<int:matricule>/<str:date_debut>/',relve_emo_view, name='relve_emo'),
    path('ATS_per/<int:matricule>/<str:date>/<int:nbrmois>',ats_per_view, name='ats_per'),
    path('profile/<matricule>',profile_view,name="profile"),
    path('attestation/<matricule>',attestation_view,name="attestation"),
    path('suprimmer_user/<matricule>',suprimmer_view,name="suprimmer_user"),
    path('contact_us/',contact_view,name="contact_us"),
    path('documents/',document_view,name="documents"),
]