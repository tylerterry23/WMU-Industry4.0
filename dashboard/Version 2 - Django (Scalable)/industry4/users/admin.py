from django.contrib import admin

# Register your models here.

from .models import Profile, Classification

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'classification')
    list_filter = ('classification', 'created')
    search_fields = ('name', 'email')
    # list_per_page = 25

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Classification)

  