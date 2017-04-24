from django.contrib import admin
from sazed_test.models import TestModel


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General',  {
            'classes': ('wide',),
            'fields': [('id',), ('created_at',), ('modified_at',)]
        }),
    ]
    list_display = ['id', 'created_at', 'modified_at']
    readonly_fields = ['id', 'created_at', 'modified_at']
