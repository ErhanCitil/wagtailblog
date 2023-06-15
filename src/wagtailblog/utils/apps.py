from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "wagtailblog.utils"

    def ready(self):
        from . import checks  # noqa
