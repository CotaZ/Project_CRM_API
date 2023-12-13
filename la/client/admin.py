from django.contrib import admin

from.models import Client, Comment

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

admin.site.register(Client, ClientAdmin)
admin.site.register(Comment)