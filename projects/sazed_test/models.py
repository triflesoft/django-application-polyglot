from django.db import models
from sazed.models import AbstractLocalizableModel


class TestModel(AbstractLocalizableModel):
    id = models.AutoField(unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        localizable_fields = ('name', 'description')
