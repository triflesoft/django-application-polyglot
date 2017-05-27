from django.forms import formsets
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from django.conf import settings


class BaseLocalizableFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseLocalizableFormSet, self).__init__(*args, **kwargs)
        self._language_codes = sorted([language[0] for language in settings.LANGUAGES], reverse=True)

    def total_form_count(self):
        return len(settings.LANGUAGES)

    def _construct_form(self, i, **kwargs):
        queryset = self.get_queryset()

        if i < len(queryset):
            try:
                self._language_codes.remove(queryset[i].language_code)
            except ValueError:
                pass

            return super(BaseLocalizableFormSet, self)._construct_form(i, **kwargs)
        else:
            return super(BaseLocalizableFormSet, self)._construct_form(i, initial={'language_code': self._language_codes.pop()}, **kwargs)


class AppAdminHelper(object):
    def _create_dynamic_model_inline_admin(self, app_label, label, model, target_model):
        from django.contrib import admin

        attrs = {
            '__module__': app_label,
            'model': model,
            'formset': formsets.formset_factory(ModelForm, formset=BaseLocalizableFormSet),
            'fk_name': 'target',
            'extra': 3}

        model_admin = type(label, (admin.TabularInline,), attrs)
        model_admin._target_model = target_model

        return model_admin

    def patch_existing_model_admin(self, **kwargs):
        from django.contrib.admin import ModelAdmin
        from ..admin import LocalizationAdminMixin

        ModelAdmin.__bases__ += (LocalizationAdminMixin,)

    def patch_existing_inline_admin(self):
        try:
            from django.contrib.admin import site
            from django.apps import apps

            for app_config in apps.get_app_configs():
                for model_label, model_info in app_config._sazed_localizable_fields.items():
                    if model_info.model in site._registry:
                        model_admin = site._registry[model_info.model]
                        setattr(model_admin, '_sazed_model_info', model_info)

                        if len(model_info.localizable_fields) > 0:
                            for field_name in sorted(model_info.localizable_fields.keys()):
                                if hasattr(model_admin, 'inlines'):
                                    inlines = list(getattr(model_admin, 'inlines'))
                                else:
                                    inlines = []

                                inline = self._create_dynamic_model_inline_admin(
                                    'sazed.admin',
                                    '{0}_{1}_LocalizationInline'.format(model_info.model.__name__, field_name.capitalize()),
                                    model_info.model._meta._sazed_localization_models[field_name],
                                    model_info.model)

                                inlines.append(inline)

                                setattr(model_admin, 'inlines', inlines)
        except:
            pass
