from django import forms


class TestModelForm(forms.ModelForm):
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


class AppAdminHelper(object):
    def _create_dynamic_admin_form(self, app_config, model, model_info):
        class Meta:
            pass

        def _init(self, *args, **kwargs):
            instance = kwargs.get('instance', None)

            if instance:
                initial = kwargs.get('initial', {})

                for property_name, field_name in model_info.localizable_fields.items():
                    initial[property_name] = instance._sazed_get_localizable(field_name)

                kwargs['initial'] = initial

            forms.ModelForm.__init__(self, *args, **kwargs)

        def _save(self, commit=True):
            instance = super(forms.ModelForm, self).save(commit=False)

            for property_name, field_name in model_info.localizable_fields.items():
                instance._sazed_set_localizable(field_name, self.cleaned_data.get(property_name, None))

            if commit:
                instance.save()

            return instance

        setattr(Meta, 'model', model)
        setattr(Meta, 'exclude', model_info.localizable_fields.values())

        attrs = {field_name: forms.CharField() for field_name in model_info.localizable_fields}
        attrs['__module__'] = app_config.label
        attrs['__init__'] = _init
        attrs['save'] = _save

        model_form = type('{0}SazedForm'.format(model._meta.label), (forms.ModelForm,), attrs)

        return model_form

    def patch_existing_model_admin(self):
        try:
            from django.contrib.admin import site
            from django.apps import apps

            for app_config in apps.get_app_configs():
                for model in app_config.get_models():
                    model_info = getattr(model._meta, '_sazed_model_info', None)

                    if model_info and model_info.has_localizable_fields() and (model in site._registry):
                        model_admin = site._registry[model]
                        setattr(model_admin, '_sazed_model_info', model_info)
                        setattr(model_admin, 'form', self._create_dynamic_admin_form(app_config, model, model_info))
        except:
            pass
