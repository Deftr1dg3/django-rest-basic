from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    # This method is called once the app is initialized
    def ready(self) -> None:
        # Import signals that will be executed automatically
        import store.signals.handlers