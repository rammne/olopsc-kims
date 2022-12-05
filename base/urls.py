from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),
    path('', views.bag, name='kims-bag'),
    path('inventory/', views.inventory, name='kims-inventory'),
    path('item/<int:pk>/', views.item_detailed_view, name='item-detail'),
    path('requests/', views.requests, name='requests'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='kims/password_reset.html'), name='password_reset'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='kims/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='kims/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='kims/password_reset_complete.html'), name='password_reset_complete'),
    path('about/', views.about_page, name='about'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('history', views.history_view, name='kims-history')
]

# path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'),