from .models import Product, User, UserReport
from .forms import PostProductForm
from django.contrib import messages
from .forms import ProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Product, Report
from django.contrib.auth.models import User
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('index', logout=True)
def newsfeed(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'newsfeed.html', {'products': products})

def post_product(request):
    if request.method == 'POST':
        form = PostProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.category = request.POST['category']
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
                # Refresh the ratings query to include the newly submitted rating
                ratings = Rating.objects.filter(rated_user=user)
                return render(request, 'profile.html', {'products': Product.objects.filter(user=user, is_active=True), 'edit_form': None, 'rating_form': None, 'user': user, 'is_owner': is_owner, 'ratings': ratings})

    if is_owner:
        edit_form = ProfileForm(instance=profile)
        rating_form = None
    else:
        edit_form = None
        rating_form = RatingForm()

    products = Product.objects.filter(user=user, is_active=True)

    return render(request, 'profile.html', {'products': products, 'edit_form': edit_form, 'rating_form': rating_form, 'user': user, 'is_owner': is_owner, 'ratings': ratings})

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Product, pk=pk)
    if listing.user == request.user:
        listing.is_active = False
        listing.save()
        messages.success(request, 'Listing deleted successfully!')
        return redirect('profile', pk=request.user.pk)
    else:
        messages.error(request, 'You do not have permission to delete this listing.')
        return redirect('profile', pk=request.user.pk)
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

@login_required
def edit_listing(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.user == request.user:
        if request.method == 'POST':
            form = PostProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Listing updated successfully!')
                return redirect('newsfeed')
        else:
            form = PostProductForm(instance=product)
        return render(request, 'edit_listing.html', {'form': form})
    else:
        messages.error(request, 'You do not have permission to edit this listing.')
        return redirect('newsfeed')

@login_required
def report_listing(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.user == request.user:
        messages.error(request, 'You cannot report your own listing.')
        return redirect('newsfeed')
    if request.method == 'POST':
        reason = request.POST.get('reason')
        report = Report.objects.create(product=product, user=request.user, reason=reason)
        messages.success(request, 'Listing reported successfully!')
        return redirect('newsfeed')
    return render(request, 'report_listing.html')

@login_required
def report_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        report = UserReport.objects.create(user=user, reported_by=request.user, reason=reason)
        messages.success(request, 'User  reported successfully!')
        return redirect('newsfeed')
    return render(request, 'report_user.html')

def category_selection(request):
    return render(request, 'category_selection.html')
def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {'products': products})

from django.shortcuts import render
from .models import Product

def electronics(request):
    products = Product.objects.filter(category='Electronics')
    return render(request, 'electronics.html', {'products': products})

def fashion(request):
    products = Product.objects.filter(category='Fashion and Beauty')
    return render(request, 'fashion.html', {'products': products})

def garden(request):
    products = Product.objects.filter(category='Home and Garden')
    return render(request, 'garden.html', {'products': products})

def sports(request):
    products = Product.objects.filter(category='Sports and Leisure')
    return render(request, 'sports.html', {'products': products})

