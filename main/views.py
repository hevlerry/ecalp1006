from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages import error


def home(request):
    return render(request, 'main/index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email address is already in use!')
                else:
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    messages.success(request, 'You have successfully registered!')
                    return redirect('login')
            else:
                messages.error(request, 'Passwords do not match!')
        else:
            messages.error(request, 'Invalid form data!')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('newsfeed')
            else:
                messages.error(request, 'Incorrect username or password')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@csrf_exempt
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        with open('contact_data.txt', 'a') as f:
            f.write(f'Name: {name}\nEmail: {email}\nMessage: {message}\n\n')

        # JavaScript alert and redirection
        return HttpResponse("""
            <html>
            <head>
                <script type="text/javascript">
                    alert('Thank you for contacting us!');
                    window.location.href = '/';  // Redirect to index.html or the homepage URL
                </script>
            </head>
            <body>
            </body>
            </html>
        """)

    return render(request, 'main/index.html')
