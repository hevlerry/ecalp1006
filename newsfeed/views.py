from .models import Product, User
from .forms import PostProductForm
from django.contrib import messages
from .forms import ProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Product
from django.contrib.auth.models import User
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('index', logout=True)
def newsfeed(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'newsfeed.html', {'products': products})

def post_product(request):
    if request.method == 'POST':
        form = PostProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, 'Your product has been successfully listed!')
            return redirect('newsfeed')
    else:
        form = PostProductForm()
    return render(request, 'post_product.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Rating
from .forms import ProfileForm, RatingForm

@login_required
def profile(request, pk):
    if pk is None:
        pk = request.user.pk
    user = get_object_or_404(User, pk=pk)
    profile = user.profile
    is_owner = user == request.user

    ratings = Rating.objects.filter(rated_user=user)

    if request.method == 'POST':
        if is_owner:
            edit_form = ProfileForm(request.POST, instance=profile)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('newsfeed')
        else:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.user = request.user
                rating.rated_user = user
                rating.save()
                messages.success(request, 'Your review has been submitted successfully!')
                return redirect('newsfeed')

    if is_owner:
        edit_form = ProfileForm(instance=profile)
        rating_form = None
    else:
        edit_form = None
        rating_form = RatingForm()

    products = Product.objects.filter(user=user)

    return render(request, 'profile.html', {'products': products, 'edit_form': edit_form, 'rating_form': rating_form, 'user': user, 'is_owner': is_owner, 'ratings': ratings})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('newsfeed')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})

