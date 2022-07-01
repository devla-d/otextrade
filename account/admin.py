from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    #form = UserAdminChangeForm
    #add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['email', 'username']
    list_filter = ['is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('country_of_residence','citizenship','gender','zipcode','city','place_of_birth','date_of_birth','phone','title','first_address','second_address','state','account_opening_reason','local_currency')}),
         (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser' )}),
      (('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (('Balance'), {'fields': ( 'balance','demo_balance','total_deposit','total_withdraw','username')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

 