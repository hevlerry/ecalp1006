from .models import Product
from .models import Profile
from django import forms
from .models import Rating


class PostProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'image', 'mobile_number', 'location')


class ProfileForm(forms.ModelForm):
    mobile_number = forms.CharField(max_length=20)

    class Meta:
        model = Profile
        fields = ('address', 'mobile_number')
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)])
        }