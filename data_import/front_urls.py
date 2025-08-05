from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('mouvements_deplaces/', views.mouvements_deplaces, name='mouvements_deplaces'),
]