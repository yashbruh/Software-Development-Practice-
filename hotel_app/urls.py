from django.urls import path
from . import views
from django.urls import include, path


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('public-homepage/', views.public_homepage, name='public_homepage'),
    path('room/<int:room_id>/', views.room_details, name='room_details'),
    path('admin-homepage/', views.admin_homepage, name='admin_homepage'),
    path('place-order/', views.place_order, name='place_order'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('verify_code/', views.verify_code_view, name='verify_code'),
    path('update-room-occupancy/', views.update_room_occupancy, name='update_room_occupancy'),
    path('reset_password/', views.reset_password_view, name='reset_password'),
    path('register/', views.register_view, name='register'),  # Add this line
    path('booking-success/', views.booking_success, name='booking-success'),
    path('reset_room_status/', views.reset_room_status, name='reset_room_status'),
    path('checkout_room/', views.checkout_room, name='checkout_room'),
    path('view_bill/', views.view_bill, name='view_bill'),


    path('checkin/', views.checkin, name='checkin'),
    path('checkin-page/', views.checkin_page, name='checkin_page'),
    path('booking-success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('fetch_details/', views.fetch_details, name='fetch_details'),
]
