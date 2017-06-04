from django.apps import AppConfig
from django.db.models.signals import class_prepared
from .helpers.admin import AppAdminHelper
from .helpers.discovery import AppDiscoveryHelper


discovery_helper = AppDiscoveryHelper()


def on_model_prepared(sender, **kwargs):
    discovery_helper.process_model(sender)


class_prepared.connect(on_model_prepared)
admin_helper = AppAdminHelper()


class SazedAppConfig(AppConfig):
    name = 'sazed'
    verbose_name = 'Sazed'

    def ready(self, *args, **kwargs):
        super(SazedAppConfig, self).ready(*args, **kwargs)

        admin_helper.patch_existing_model_admin()
