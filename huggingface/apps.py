from django.apps import AppConfig


class HuggingfaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'huggingface'

    def ready(self):
        from .utils import huggingface_login
        huggingface_login()
