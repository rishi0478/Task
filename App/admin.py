from django.contrib import admin
from App.models import Profile,Login_model,student_db
# Register your models here.
@admin.register(Profile)
class Page_Admin(admin.ModelAdmin):
    list_display = ['user','auth_token','is_active','created_at']

@admin.register(Login_model)
class log_mod(admin.ModelAdmin):
    list_display =  ['username','password']

@admin.register(student_db)
class Student_data(admin.ModelAdmin):
    list_display = ['name','roll_no']
