from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurants'
    def ready(self):
        # Importez les signaux ici pour les enregistrer
        from restaurants import signals
