
from django.urls import path, re_path

from Marketplace_webpage.views import home
from newsfeed.views import newsfeed, post_product, profile, edit_profile, logout_view, delete_listing, \
    category_selection, electronics, fashion, garden, sports

urlpatterns = [
    path('', newsfeed, name='newsfeed'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='index'),
    path('post/', post_product, name='post_product'),
    path('profile/', profile, name='profile'),
    path('profile/<pk>/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('delete-listing/<pk>/', delete_listing, name='delete_listing'),
    path('categories/', category_selection, name='category_selection'),
    path('electronics/', electronics, name='electronics'),
    path('fashion/', fashion, name='fashion'),
    path('garden/', garden, name='garden'),
    path('sports/', sports, name='sports'),
]