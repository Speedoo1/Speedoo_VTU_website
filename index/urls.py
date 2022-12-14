from django.urls import path
from . import views

app_name = 'index'
urlpatterns = [
    path('', views.index, name='index'),
    path('airtime/', views.airtime, name='airtime'),
    path('dataplan/', views.dataplan, name='data'),
    path('waec/', views.waec, name='waec'),

    path("login/", views.loging, name="loging"),
    path('logout/', views.logoutpage, name='logout'),
    path('create_an_account', views.registration, name="create"),
    path('profile/', views.profiles, name='profile'),
    path('fundwallet/', views.fundwallet, name='fund'),
    path('print-recharge-card/', views.print, name="print"),
    path('updateprofile/', views.updateprofile, name="updateprofile"),
    path("Pay_Electricity_bill/", views.electricity, name="electric"),
    path('pending_fund', views.pendigwallet, name="pend"),
    path('confirm-payment/', views.confirmpayment, name='confirm-payment'),
    path('ffddsawweaqwer4432144567iijhgvvcxr64w/', views.payment, name='payment'),
    path('cable_tv_subscription/', views.cabletv, name='cable'),
    path('transaction-history/', views.history, name="history"),
    path('transaction-history/<str:pk>', views.singleHistory, name="history-single")

]
