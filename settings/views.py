from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import UpdateView


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'settings/account.html'
    success_url = reverse_lazy('settings:account')

    def get_object(self, queryset=None):
        return self.request.user
