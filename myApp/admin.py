from django.contrib import admin

# Register your models here.
from .models import UserFile, Feature, FeatureValidation, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    admin interface for StudentInformation.
    """
    list_display = ('id', 'email')


@admin.register(UserFile)
class UserFileAdmin(admin.ModelAdmin):
    """
    admin interface for StudentInformation.
    """
    list_display = ('id', 'user', 'epic', 'error_msg', 'start_date', 'status')


@admin.register(FeatureValidation)
class FeatureValidationAdmin(admin.ModelAdmin):
    """
     admin interface for StudentInformation.
     """
    list_display = ('feature', 'msg')


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    """
     admin interface for StudentInformation.
     """
    list_display = ('id', 'user_file', 'name')
