class LocalizationAdminMixin:
    def __init__(self, *args, **kwargs):
        super(LocalizationAdminMixin, self).__init__(*args, **kwargs)

    def get_queryset(self, request):
        fields = self._sazed_model_info.localizable_fields

        queryset = super(LocalizationAdminMixin, self).get_queryset(request)

        for relation_name in fields.values():
            queryset = queryset.prefetch_related(relation_name)

        return queryset
