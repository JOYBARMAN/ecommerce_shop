from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="Shophome"),
    path('contact/', views.contact, name="Shopcontact"),
    path('about/', views.about, name="Shopabout"),
    path('search/', views.search, name="Shopsearch"),
    path('products/<int:myid>', views.productview, name="Shopproductview"),
    path('checkpoint/', views.checkpoint, name="Shopcheckpoint"),
    path('tracker/', views.tracker, name="Shoptracker"),
]
