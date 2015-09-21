from django.contrib import admin
from toolshare.models import ToolShareUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from toolshare.models import ToolShareUser
# Register your models here.

#admin.site.register(ToolShareUser)

class ToolShareUserInline(admin.StackedInline):
    model = ToolShareUser
    can_delete = False
    verbose_name_plural = 'tool share user'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ToolShareUserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)