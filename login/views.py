from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from .forms import registreform


def login_view(request):
    if request.method == 'POST':
        logform = AuthenticationForm(request, data=request.POST)
        if logform.is_valid():
            user = logform.get_user()
            login(request, user)
            
            return redirect('dashboard')
    else:
        logform = AuthenticationForm()
    return render(request, 'login/signin.html', {'logform': logform})


def signup_view(request):
    if request.method == 'POST':
        form = registreform(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('signin')
    else:
        form = registreform()
    return render(request, 'login/signup.html', {'form': form})


def userlogout(request):
    logout(request)
    return redirect('signin')
