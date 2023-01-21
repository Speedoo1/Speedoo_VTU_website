from django.urls import path

from api import views

urlpatterns = [
    path('', views.base, name='base'),
    path('history/<str:pk>', views.historydatas),
    path('balance/', views.walletballance),
    path('airtime/', views.buyairtime),
    path('data/', views.buydata)

]
