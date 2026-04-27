from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),

    path('testimonials/', views.testimonials, name='admin_testimonials'),
    path('testimonials/add/', views.add_testimonial, name='admin_add_testimonial'),
    path('admin/testimonials/edit/<int:id>/', views.edit_testimonial, name='admin_edit_testimonial'),
    path('admin/testimonials/delete/<int:id>/', views.delete_testimonial, name='admin_delete_testimonial'),

    path('amenities/', views.amenities, name='admin_amenities'),
    path('amenities/add/', views.add_amenity, name='admin_add_amenity'),
    path('amenities/edit/<int:id>/', views.edit_amenity, name='admin_edit_amenity'),
    path('amenities/delete/<int:id>/', views.delete_amenity, name='admin_delete_amenity'),

    path('faqs/', views.admin_faqs, name='admin_faqs'),
    path('faqs/add/', views.admin_add_faq, name='admin_add_faq'),
    path('faqs/edit/<int:id>/', views.admin_edit_faq, name='admin_edit_faq'),
    path('faqs/delete/<int:id>/', views.admin_delete_faq, name='admin_delete_faq'),

    path('gallery/', views.admin_gallery, name='admin_gallery'),
    path('gallery/add/', views.add_gallery, name='add_gallery'),
    path('gallery/edit/<int:pk>/', views.edit_gallery, name='edit_gallery'),
    path('gallery/delete/<int:pk>/', views.delete_gallery, name='delete_gallery'),

    path('admin-panel/contact-us/', views.admin_contactus, name='admin_contactus'),
    path('admin-panel/contact-us/edit/', views.admin_edit_contactus, name='admin_edit_contactus'),
    path('admin-panel/enquiries', views.admin_enquiries, name='admin_enquiries'),

    path('admin/restaurant/', views.admin_restaurant, name='admin_restaurant'),
    path('admin/restaurant/add/', views.admin_add_restaurant, name='admin_add_restaurant'),
    path('admin/restaurant/edit/<int:id>/', views.admin_edit_restaurant, name='admin_edit_restaurant'),
    path('admin/restaurant/delete/<int:id>/', views.admin_delete_restaurant, name='admin_delete_restaurant'),

    path('admin/rooms/', views.admin_rooms, name='admin_rooms'),
    path('admin/rooms/add/', views.admin_add_room, name='admin_add_room'),
    path('admin/rooms/edit/<int:id>/', views.admin_edit_room, name='admin_edit_room'),
    path('admin/rooms/delete/<int:id>/', views.admin_delete_room, name='admin_delete_room'),

    path('admin/guests/', views.admin_guests, name='admin_guests'),
    path('admin/guests/add/', views.admin_add_guest, name='admin_add_guest'),
    path('admin/guests/edit/<int:guest_id>/', views.admin_edit_guest, name='admin_edit_guest'),
    path('admin/guests/delete/<int:guest_id>/', views.admin_delete_guest, name='admin_delete_guest'),

    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin/bookings/add/', views.admin_add_booking, name='admin_add_booking'),
    path('admin/bookings/edit/<int:id>/', views.admin_edit_booking, name='admin_edit_booking'),
    path('admin/bookings/delete/<int:id>/', views.admin_delete_booking, name='admin_delete_booking'),

    path('coupons/', views.admin_coupon, name='admin_coupon'),
    path('coupons/add/', views.admin_add_coupon, name='admin_add_coupon'),
    path('coupons/edit/<int:id>/', views.admin_edit_coupon, name='admin_edit_coupon'),
    path('coupons/delete/<int:id>/', views.admin_delete_coupon, name='admin_delete_coupon'),

    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/profile/', views.admin_profile, name='admin_profile'),

    path('registered_users/', views.admin_registered_users, name='admin_registered_users'),
    path('registered_users/add/', views.admin_add_registered_user, name='admin_add_registered_user'),
    path('registered_users/edit/<int:id>/', views.admin_edit_registered_user, name='admin_edit_registered_user'),
    path('registered_users/delete/<int:id>/', views.admin_delete_registered_user, name='admin_delete_registered_user'),

    path("menu/", views.admin_menu, name="admin_menu"),
    path("menu/add/", views.admin_add_menu, name="admin_add_menu"),
    path("menu/edit/<int:id>/", views.admin_edit_menu, name="admin_edit_menu"),
    path("menu/delete/<int:id>/", views.admin_delete_menu, name="admin_delete_menu"),
]
