from django.contrib import admin
from .models import Alarm
from unfold.admin import ModelAdmin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
# Register your models here.
@admin.register(Alarm)
class AlarmAdmin(ModelAdmin):
    list_display = ('time', 'date', 'days', 'enabled', 'is_active', 'timezone')
    list_filter = ('enabled', 'is_active', 'timezone')
    search_fields = ('time', 'date', 'days')
    ordering = ('time',)


admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)


    # form = UserChangeForm
    # # add_form = UserCreationForm
    # change_password_form = AdminPasswordChangeForm



@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass