from django.db import models
from django.conf import settings


def _localizable_value_str(self):
    return ''


class AppModelHelper(object):
    def _create_dynamic_model(self, app_label, label, attributes=None, options=None):
        class Meta:
            pass

        setattr(Meta, 'app_label', app_label)

        if options is not None:
            for key, value in options.items():
                setattr(Meta, key, value)

        attrs = {'__module__': 'sazed', 'Meta': Meta}

        if attributes:
            attrs.update(attributes)

        model = type(label, (models.Model,), attrs)

        return model

    def _create_localizable_value_model(self, model_info, field_name, relation_name):
        dynamic_model = self._create_dynamic_model(
            'sazed',
            'LocalizableField_{0}_{1}_{2}'.format(model_info.app_config.label.capitalize(), model_info.model.__name__, field_name),
            attributes={
                'target': models.ForeignKey(
                    model_info.model._meta.label,
                    related_name=relation_name,
                    on_delete=models.CASCADE),
                'language_code': models.CharField(max_length=16, choices=settings.LANGUAGES),
                'value': models.CharField(max_length=255),
                '__str__': _localizable_value_str
            },
            options={
                'verbose_name': field_name,
                'unique_together': [('target', 'language_code')],
                'index_together': [('target', 'language_code', 'value')]
            })

        def _get_value(self):
            related_manager = getattr(self, relation_name)

            return self._get_localizable_value(related_manager, relation_name)

        def _set_value(self, value):
            related_manager = getattr(self, relation_name)

            return self._set_localizable_value(related_manager, relation_name, value)

        def _del_value(self):
            related_manager = getattr(self, relation_name)

            return self._del_localizable_value(related_manager, relation_name)

        setattr(model_info.model, field_name, property(_get_value, _set_value, _del_value))

        return dynamic_model

    def __init__(self, *args, **kwargs):
        from collections import OrderedDict

        self.all_permission_models = OrderedDict()

    def create_localization_models(self, **kwargs):
        from collections import OrderedDict
        from django.apps import apps

        for app_config in apps.get_app_configs():
            app_config._sazed_localization_models = OrderedDict()

            for model_label, model_info in app_config._sazed_localizable_fields.items():
                model_info.model._meta._sazed_localization_models = {}

                for field_name, relation_name in model_info.localizable_fields.items():
                    dynamic_model = self._create_localizable_value_model(model_info, field_name, relation_name)

                    model_info.model._meta._sazed_localization_models[field_name] = dynamic_model
                    app_config._sazed_localization_models[dynamic_model._meta.label] = dynamic_model
