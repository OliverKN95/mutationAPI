from django.contrib import admin
from .models import logs

# Register your models here.
@admin.register(logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('has_mutation', 'success', 'timestamp')
    list_filter = ('has_mutation', 'success')
    search_fields = ['has_mutation', 'success']