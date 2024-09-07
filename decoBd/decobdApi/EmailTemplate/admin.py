from django.contrib import admin
from .models import EmailTemplate
# Register your models here.

class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('message_type','subject','is_active')  # Columns to display in the list view
    list_filter = ('message_type', 'is_active')  # Filters for message type and active status
    search_fields = ('subject', 'message_type')  # Add search functionality based on subject and message type
    

admin.site.register(EmailTemplate, EmailTemplateAdmin)
