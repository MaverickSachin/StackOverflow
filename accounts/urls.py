from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

app_name = 'accounts'

urlpatterns = [
    # /accounts/
    path('signup/', views.signup, name='signup'),

    # /accounts/logout/
    path('logout/', LogoutView.as_view(), name='logout'),

    # /accounts/login/
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # /accounts/reset/
    path('reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password_reset'),

    # /accounts/reset/done/
    path('reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),

    # /accounts/reset/confirm/<uidb64>/<token>/
    path('reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),

    # /accounts/reset/complete/
    path('reset/complete/', PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
