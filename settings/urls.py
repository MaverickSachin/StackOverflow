from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .views import UserUpdateView

app_name = 'settings'

urlpatterns = [
    # /settings/password/
    path('password/', PasswordChangeView.as_view(
        template_name='settings/password_change.html',
        success_url=reverse_lazy('settings:password_change_done')
    ), name='password_change'),

    # settings/password/done/
    path('password/done/', PasswordChangeDoneView.as_view(
        template_name='settings/password_change_done.html'
    ), name='password_change_done'),

    # settings/account/
    path('account/', UserUpdateView.as_view(), name='account'),
]
