from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Brand, CarModel, Car, CarImage, Inquiry, Testimonial, Wishlist


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand']
    list_filter = ['brand']
    search_fields = ['name', 'brand__name']


class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3
    max_num = 20
    min_num = 3


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand', 'model', 'year', 'price', 'fuel_type', 'transmission', 'status', 'is_featured', 'created_at']
    list_filter = ['status', 'is_featured', 'fuel_type', 'transmission', 'body_type', 'brand', 'ownership']
    search_fields = ['title', 'brand__name', 'model__name', 'variant']
    list_editable = ['status', 'is_featured']
    inlines = [CarImageInline]
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'brand', 'model', 'year', 'variant', 'color', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price')
        }),
        ('Specifications', {
            'fields': ('mileage', 'fuel_type', 'transmission', 'body_type', 'ownership')
        }),
        ('Registration & Insurance', {
            'fields': ('registration_year', 'insurance_validity', 'insurance_type', 'rto')
        }),
        ('Location', {
            'fields': ('village_area', 'city')
        }),
        ('Seller', {
            'fields': ('seller', 'contact_name', 'contact_number')
        }),
        ('Status', {
            'fields': ('status', 'is_featured')
        }),
    )


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ['car', 'is_primary', 'created_at']
    list_filter = ['is_primary']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'subject', 'car', 'created_at']
    list_filter = ['subject', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'created_at']
    list_filter = ['created_at']
