from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'image', 'mobile_number', 'location', 'user')
    search_fields = ('title', 'description', 'price', 'mobile_number', 'location', 'user__username')
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        queryset.delete()


admin.site.register(Product, ProductAdmin)
