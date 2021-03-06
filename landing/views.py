from django.shortcuts import render
from .forms import UPC
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
import requests


# def home(request):
#     # upc = None
#     # if request.method == 'POST':
#     #     upc = request.POST
#     #     print(upc)
#     #     upc_id = upc.get('input_upc')
#     #     print('UPC = ', upc_id)
#
#     if request.method == "POST":
#         # upc = request.POST.get('input_upc')
#
#         data = request.POST
#         print('upc =', data['upc'])
#
#
#         # text = data.
#         # print('text =', text)
#     return render(request, 'home.html', locals())

def home(request):
    name = ''
    form = UPC(request.POST or None)
    if request.POST and form.is_valid():
        print('YES is_valid')
        data = form.cleaned_data
        print(data['upc'])
        upc = data['upc']

        r = requests.get('http://api.walmartlabs.com/v1/items',
                         params={'apiKey': '5tkgtq74ffgptjd884pmuj8t', 'upc': upc})
        if r.status_code == 200:
            # print(r.json().get('items').pop().get('name'))
            name = r.json().get('items').pop().get('name')
        else:
            print('Error! UPC not found')
            name = 'Error! UPC not found'
    else:
        print("NO valid")

    print(name)

    return render(request, 'home.html', locals())


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        print(self.user)
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")
