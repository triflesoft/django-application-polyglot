from django.conf import settings
from django.db import models

models.options.DEFAULT_NAMES = \
    models.options.DEFAULT_NAMES + \
    ('localizable_fields', )

DEFAULT_LANGUAGE_CODE = settings.LANGUAGE_CODE


class AbstractLocalizableMixin(object):
    def __init__(self, *args, **kwargs):
        from django.utils import translation

        super(AbstractLocalizableMixin, self).__init__(*args, **kwargs)

        self._sazed_language_code = translation.get_language() or DEFAULT_LANGUAGE_CODE
        self._sazed_original_values = {}

    def _sazed_get_localizable(self, field_name):
        localizations = getattr(self, field_name, None)

        if localizations:
            for language_code in (self._sazed_language_code, DEFAULT_LANGUAGE_CODE):
                localization_text = localizations.get(language_code, None)

                if localization_text:
                    self._sazed_original_values[field_name] = localization_text

                    return localization_text

            for localization_text in localizations.values():
                self._sazed_original_values[field_name] = localization_text

                return localization_text

        return ''

    def _sazed_set_localizable(self, field_name, value):
        localizations = getattr(self, field_name, None)

        if value and (value != self._sazed_original_values.get(field_name, None)):
            if localizations:
                localizations[self._sazed_language_code] = value
            else:
                localizations = {self._sazed_language_code: value}
                setattr(self, field_name, localizations)
