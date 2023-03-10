from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_at',)

admin.site.register(Todo, TodoAdmin)
