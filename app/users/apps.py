from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "app.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import app.users.signals  # noqa F401
        except ImportError:
            pass
        from actstream import registry

        registry.register(self.get_model("User"))
