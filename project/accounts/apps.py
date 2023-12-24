"""App configuration for accounts app"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    App configuration for accounts app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self) -> None:
        import accounts.signals
