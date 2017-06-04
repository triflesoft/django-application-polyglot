class ModelInfo(object):
    def __init__(self, model, localizable_fields):
        self.model = model
        self.localizable_fields = localizable_fields

    def has_localizable_fields(self):
        return len(self.localizable_fields) > 0


class AppDiscoveryHelper(object):
    def __init__(self):
        self._model_infos = {}

    def _create_property(self, model, property_name, field_name):
        def _property_get(self):
            return self._sazed_get_localizable(field_name)

        def _property_set(self, value):
            return self._sazed_set_localizable(field_name, value)

        setattr(model, property_name, property(_property_get, _property_set))

    def process_model(self, model):
        from ..models import AbstractLocalizableMixin
        from django.contrib.postgres import fields

        if hasattr(model._meta, 'app_config') and model._meta.app_config:
            if not model._meta.label_lower in self._model_infos:
                if hasattr(model._meta, 'localizable_fields'):
                    localizable_fields = {
                        field_name: '_{0}_localizations'.format(field_name) for field_name in getattr(model._meta, 'localizable_fields')}
                else:
                    localizable_fields = {}

                if len(localizable_fields) > 0:
                    model.__bases__ += (AbstractLocalizableMixin,)

                    for property_name, field_name in localizable_fields.items():
                        field = fields.HStoreField(field_name, blank=True, null=True)
                        field.contribute_to_class(model, field_name)
                        self._create_property(model, property_name, field_name)

                model_info = ModelInfo(model, localizable_fields)
                model._meta._sazed_model_info = model_info
                self._model_infos[model._meta.label_lower] = model_info
