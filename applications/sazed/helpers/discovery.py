class ModelInfo(object):
    def __init__(self, app_config, model, localizable_fields):
        from ..models import AbstractLocalizableMixin
        self.app_config = app_config
        self.model = model
        self.localizable_fields = set(str(localizable_field) for localizable_field in localizable_fields)

        if len(self.localizable_fields) > 0:
            self.model.__bases__ += (AbstractLocalizableMixin,)


class AppDiscoveryHelper(object):
    def __init__(self):
        self._model_infos = {}

    def discover_localizations(self):
        from collections import OrderedDict
        from django.apps import apps

        for app_config in apps.get_app_configs():
            app_config._sazed_localizable_fields = OrderedDict()

            for model in app_config.get_models():
                if hasattr(model._meta, 'localizable_fields'):
                    localizable_fields = getattr(model._meta, 'localizable_fields')
                else:
                    localizable_fields = []

                model_info = ModelInfo(app_config, model, localizable_fields)
                app_config._sazed_localizable_fields[model._meta.label_lower] = model_info
