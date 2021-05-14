from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
User = get_user_model()


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
    list_display = ['id', 'email', 'phone_number', 'is_active', 'is_staff', ]
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
            'fields': ('full_name', 'email', 'password',
                       'phone_number', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'firebase_uuid',
                       'profile_picture', 'push_notification', 'gender',
                       )}
         ),
    )

    filter_horizontal = ()


admin.site.register(User, UserAdmin)
