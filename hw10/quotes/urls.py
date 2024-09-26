from django.urls import path
from django.contrib.auth import views as auth_views
from quotes import views as quotes_views
from . import views

app_name = 'quotes'

urlpatterns = [
    # Маршрути для автентифікації
    path('', views.home, name='home'),
    path('signup/', quotes_views.signupuser, name='signupuser'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='loginuser'),
    path('logout/', auth_views.LogoutView.as_view(), name='logoutuser'),
    path('profile/', views.profile, name='profile'),

    # Маршрути для авторів та цитат
    path('authors/', views.author_list, name='author_list'),
    path('quotes/', views.quote_list, name='quote_list'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('author/<str:author_id>/', views.author_page, name='author_page'),  # Маршрут до сторінки з деталями автора
    path('author/<str:author_id>/quotes/', views.author_quotes, name='author_quotes'),  # Маршрут до сторінки з цитатами автора

    # Маршрути для скидання пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
