from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # /admin/
    path("admin/", admin.site.urls),

    # /boards/
    path('boards/', include('boards.urls', namespace='boards')),

    # /accounts/
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # /settings/
    path('settings/', include('settings.urls', namespace='settings')),
]
