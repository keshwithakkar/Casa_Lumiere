"""
URL configuration for casa_lumeria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from .views import restaurant_page, about_us, amenities, gallery, faq, contact, terms, testimonial, rooms, book
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   
    path('', views.home, name='home'),
    path('restaurant/', views.restaurant_page, name='restaurant_page'),
    path('about/', about_us, name='about_us'),
    path('amenities/', amenities, name='amenities'),
    path('gallery/', gallery, name='gallery'),
    path('faq/', faq, name='faq'),
    path('contact/', contact, name='contact'),
    path('terms/', terms, name='terms'),
    path('testimonial/', testimonial, name='testimonial'),
    path('rooms/', rooms, name='rooms'),
    path('book/', book, name='book'),

    path('signup/', views.signup, name='signup'),
    path("login/", views.login_view, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("my_bookings/", views.my_bookings, name="my_bookings"),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('profile/', views.manage_profile, name='manage_profile'),

    path('menu/', views.menu, name='menu'),

    path("invoice/<int:booking_id>/", views.invoice_page, name="invoice"),

    path("notifications/", views.notifications, name="notifications"),

]