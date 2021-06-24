from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
User = get_user_model()
from .models import (
    Shipping,
    FacebookDataDelete,
)


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = ['id', 'email', 'phone_number', 'is_active', 'is_staff', 'reward_points']
    ordering = ("email",)
    fieldsets = (
        (
            'General',
            {
                'fields': (
                    'full_name',
                    'password',
                    'phone_number',
                    'date_joined',
                    'firebase_uuid',
                    'profile_picture',
                    'gender',
                    'reward_points',
                )
            }),
        (
            'Permissions',
            {
                'fields': (
                    'is_superuser',
                    'is_staff',
                    'is_active',
                    'push_notification',
                )
            }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'email', 'password', 'phone_number', 'is_superuser', 'is_staff',
                        'is_active', 'date_joined', 'firebase_uuid',
                       'profile_picture', 'push_notification', 'gender', 'reward_points',
                       )}
         ),
    )

    filter_horizontal = ()


admin.site.register(User, UserAdmin)


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'area','street_address','is_default',)
    search_fields = ('user__email', 'first_name', 'phone_no', 'email','street_address', )
    list_filter = ('area', 'is_default',)
    fieldsets = (
        (
            'General', {
            'fields': (
                'user', 'area', 'street_address', 'postal_code', 'first_name', 'last_name', 'email', 'phone_no', 'is_default',
            )
        }),
        (
            'Important Dates', {
            'fields': (
                'created_on', 'modified_on',
            ),
        }),
    )


@admin.register(FacebookDataDelete)
class FacebookDataDeleteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'uuid', 'status')
    list_filters = ('user',)
