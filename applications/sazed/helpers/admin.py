def _formfield_for_foreignkey(self, db_field, request=None, **kwargs):
    from django.contrib.contenttypes.models import ContentType

    field = super(type(self), self).formfield_for_foreignkey(db_field, request, **kwargs)

    if db_field.name == 'permission':
        field.queryset = field.queryset.filter(content_type=ContentType.objects.get_for_model(self._target_model))

    return field


class AppAdminHelper(object):
    def _create_dynamic_model_inline_admin(self, app_label, label, model, target_model):
        from django.contrib import admin

        attrs = {
            '__module__': app_label,
            'model': model,
            'fk_name': 'target'}

        model_admin = type(label, (admin.TabularInline,), attrs)
        model_admin.formfield_for_foreignkey = _formfield_for_foreignkey
        model_admin._target_model = target_model

        return model_admin

    def patch_exiting_admin_inline(self):
        try:
            from django.contrib.admin import site
            from django.apps import apps

            for app_config in apps.get_app_configs():
                for model_label, model_info in app_config._talos_permissions.items():
                    if model_info.model in site._registry:
                        model_admin = site._registry[model_info.model]
                        setattr(model_admin, '_talos_model_info', model_info)

                        if model_info.has_object_permissions():
                            if hasattr(model_admin, 'inlines'):
                                inlines = getattr(model_admin, 'inlines')
                            else:
                                inlines = []

                            inline = self._create_dynamic_model_inline_admin(
                                'talospermissions.admin',
                                '{0}ObjectPermissionsInline'.format(model_info.model.__name__),
                                model_info.model._meta.object_permission_model,
                                model_info.model)

                            inlines.append(inline)

                            setattr(model_admin, 'inlines', inlines)
        except:
            pass
