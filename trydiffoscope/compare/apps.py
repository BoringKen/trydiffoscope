from django.apps import AppConfig

class CompareConfig(AppConfig):
    name = 'trydiffoscope.compare'

    def ready(self):
        from . import signals # noqa
