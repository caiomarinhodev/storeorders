import uuid

from allauth.account.forms import LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView

from app.models import Token
from app.request_api import login_user, register_user


class RegisterView(FormView):
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm
    success_url = '/'

    def generate_email(self):
        key = uuid.uuid1()
        return '{}@{}'.format(key, 'teste.com')

    def form_valid(self, form):
        data = form.cleaned_data
        data['email'] = self.generate_email()
        res = register_user(data['username'], data['username'], data['email'],
                            data['password1'])
        if 'id' in res:
            user = form.save(self.request)
            user.is_active = True
            user.save()
            messages.success(self.request, 'Usuário criado com sucesso')
            return super(RegisterView, self).form_valid(form)
        else:
            messages.error(self.request, 'Houve algum erro, tente novamente')
            return super(RegisterView, self).form_invalid(form)


class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        username = data['username']
        password = data['password']
        res = login_user(username, password)
        if 'message' in res:
            user = authenticate(username=username, password=password)
            token = Token(user=user, token=res['token'])
            token.save()
            login(self.request, user)
            messages.success(self.request, 'Login efetuado com sucesso')
            return super(LoginView, self).form_valid(form)
        else:
            messages.error(self.request, 'Houve algum erro, tente novamente')
            return super(LoginView, self).form_invalid(form)


class LogoutView(RedirectView):
    template_name = 'accounts/logout.html'
    form_class = LoginForm

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        user = self.request.user
        token = Token.objects.filter(user=user).first()
        token.delete()
        logout(request)
        messages.success(self.request, 'Logout efetuado com sucesso')
        return super(LogoutView, self).get(request, *args, **kwargs)
