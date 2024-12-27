from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    
    home, register_choice, register_parent, babysitter_register,search_babysitters,voir_reservations_babysitter,
    update_babysitter_profile,babysitter_profile,babysitter_detail,parent_reservations,update_parent_profile,
    login_view, parent_dashboard, babysitter_dashboard,custom_logout,cancel_reservation,create_reservation_for,
    notifications_parent,notifications_babysitter,mark_notification_as_read
)

urlpatterns = [
    path('', home, name='home'), 
    path('register/', register_choice, name='register_choice'),
    path('register/parent/', register_parent, name='register_parent'),
    path('register/babysitter/', babysitter_register, name='babysitter_register'),

    path('login/', login_view, name='login'),
    path('dashboard/parent/', parent_dashboard, name='parent_dashboard'),
    path('dashboard/babysitter/', babysitter_dashboard, name='babysitter_dashboard'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', custom_logout, name='logout'),
    path('search/', search_babysitters, name='search_babysitters'),
    path('annuler/<int:babysitter_id>/', cancel_reservation, name='cancel_reservation'),
    path('reservation/<int:babysitter_id>/', create_reservation_for, name='create_reservation_for'),
    path('babysitter/profile/',babysitter_profile, name='babysitter_profile'),
    path('babysitter/profile/update/', update_babysitter_profile, name='update_babysitter_profile'),
    path('babysitter/<int:babysitter_id>/', babysitter_detail, name='babysitter_detail'),
    path('reservations/<int:babysitter_id>/', voir_reservations_babysitter, name='voir_reservations_babysitter'),
    path('parent_reservations/<int:parent_id>/', parent_reservations, name='parent_reservations'),
    path('update-profile/', update_parent_profile, name='update_parent_profile'),
    path('notifications/parent/', notifications_parent, name='notifications_parent'),
    path('notifications/babysitter/', notifications_babysitter, name='notifications_babysitter'),
    path('notifications/mark_as_read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
]

