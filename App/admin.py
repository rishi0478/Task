from django.contrib import admin
from App.models import Profile
# Register your models here.
@admin.register(Profile)
class Page_Admin(admin.ModelAdmin):
    list_display = ['user','auth_token','is_active','created_at']
