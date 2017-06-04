from django import forms
from django.contrib import admin
from sazed_test.models import TestModel


class TestModelForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.CharField()

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)

        if instance:
            initial = kwargs.get('initial', {})
            initial['name'] = instance.name
            initial['description'] = instance.description
            kwargs['initial'] = initial

        super(TestModelForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(TestModelForm, self).save(commit=False)
        instance.name = self.cleaned_data.get('name', None)
        instance.description = self.cleaned_data.get('description', None)

        if commit:
            instance.save()

        return instance

    class Meta:
        model = TestModel
        exclude = ('_name_localizations', '_description_localizations')


@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General',  {
            'classes': ('wide',),
            'fields': [('name',), ('description',)]
        }),
        ('Audit',  {
            'classes': ('wide',),
            'fields': [('id',), ('modified_at',)]
        }),
    ]
    list_display = ['id', 'created_at', 'modified_at', 'name']
    readonly_fields = ['id', 'created_at', 'modified_at']
    #form = TestModelForm
