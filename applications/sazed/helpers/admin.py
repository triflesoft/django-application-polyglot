class AppAdminHelper(object):
    def _create_dynamic_model_inline_admin(self, app_label, label, model, target_model):
        from django.contrib import admin

        attrs = {
            '__module__': app_label,
            'model': model,
            'fk_name': 'target',
            'extra': 0}

        model_admin = type(label, (admin.TabularInline,), attrs)
        model_admin._target_model = target_model

        return model_admin

    def patch_exiting_admin_inline(self):
        try:
            from django.contrib.admin import site
            from django.apps import apps

            for app_config in apps.get_app_configs():
                for model_label, model_info in app_config._sazed_localizable_fields.items():
                    if model_info.model in site._registry:
                        model_admin = site._registry[model_info.model]
                        setattr(model_admin, '_sazed_model_info', model_info)

                        for localizable_field in sorted(model_info.localizable_fields):
                            if hasattr(model_admin, 'inlines'):
                                inlines = list(getattr(model_admin, 'inlines'))
                            else:
                                inlines = []

                            inline = self._create_dynamic_model_inline_admin(
                                'sazed.admin',
                                '{0}_{1}_LocalizationInline'.format(model_info.model.__name__, localizable_field.capitalize()),
                                model_info.model._meta._sazed_localization_models[localizable_field],
                                model_info.model)

                            inlines.append(inline)

                            setattr(model_admin, 'inlines', inlines)
        except:
            pass
