from django.apps import AppConfig

from sazed.helpers.admin import AppAdminHelper
from sazed.helpers.discovery import AppDiscoveryHelper
from sazed.helpers.models import AppModelHelper

admin_helper = AppAdminHelper()
discovery_helper = AppDiscoveryHelper()
model_helper = AppModelHelper()


class SazedAppConfig(AppConfig):
    name = 'sazed'
    verbose_name = 'Sazed'

    def ready(self, *args, **kwargs):
        super(SazedAppConfig, self).ready(*args, **kwargs)

        discovery_helper.discover_localizations()
        model_helper.create_localization_models()
        admin_helper.patch_exiting_admin_inline()
