from . import forms
from . import models
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

def landing(request):
    restaurants = models.Restaurant.objects.all()
    return render(request, 'main/landing.html', {'restaurants':restaurants})

def login_request(request):
    if request.method == 'POST':
        form = forms.Login(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('/')
        else:
            return render(request=request,
                          template_name="main/login.html",
                          context={"form": form, "error": "Incorrect Username or Password"})
    form = forms.Login()
    return render(request=request,
                  template_name="main/login.html",
                  context={"form": form})

def register(request):
    if request.method == "POST":
        form = forms.Registration(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("/")

        return render(request=request,
                      template_name="main/register.html",
                      context={"form": form})
    form = forms.Registration()
    return render(request=request,
                  template_name="main/register.html",
                  context={"form": form})

def logout_request(request):
    try:
        referer = request.META.get('HTTP_REFERER', '').split('/')[-2]
    except:
        referer = ""
    logout(request)
    return redirect(f'/{referer}')


def check_superuser(request):
    return HttpResponse(request.user.is_superuser)

def check_staff_user(request):
    return HttpResponse(request.user.is_staff)

def handle_404(request, exception):
    return render(request, 'main/404.html')

def handle_500(request):
    return render(request, 'main/500.html')

def handle_403(request, exception):
    return render(request, 'main/403.html')