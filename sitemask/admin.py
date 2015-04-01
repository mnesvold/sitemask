from django.contrib import admin

from .models import Mask

class MaskAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'image'),
        }),
        ('Visibility', {
            'fields': ('effective', 'expiration'),
        }),
    )
    list_display = ('title', 'subtitle', 'image', 'effective', 'expiration')
    ordering = ('-effective', 'expiration')
    search_files = ('title', 'subtitle', 'image')
    view_on_site = False

admin.site.register(Mask, MaskAdmin)
