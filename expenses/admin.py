# admin.py
from django.contrib import admin
from .models import Expense, ManagerProfile, ManagerOnboarding

admin.site.register(Expense)

@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'phone', 'pg_property', 'created_at')
    search_fields = ('full_name', 'user__username', 'phone', 'pg_property')


@admin.register(ManagerOnboarding)
class ManagerOnboardingAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer1', 'answer2', 'answer3', 'answer4', 'answer5', 'created_at')
    search_fields = ('user__username', 'answer1', 'answer2')

from .models import Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'tenant_type', 'status', 'city')
    search_fields = ('name', 'city')
    inlines = [PropertyImageInline]

admin.site.register(PropertyImage)