from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LearngualConfig(AppConfig):
    name = "learngual"
    verbose_name = _("Learngual")

    def ready(self):
        try:
            import learngual.signals  # noqa F401
        except ImportError:
            pass
