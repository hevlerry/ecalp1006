from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model


User = get_user_model()


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    mobile_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

def profile_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'profile.html', {'user': user})

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

from django.db import models
from django.contrib.auth.models import User

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rated_user')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} rated {self.rated_user.username} {self.rating}/5'