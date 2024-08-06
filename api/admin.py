from django.contrib import admin
from django.apps import apps

# Get the app configuration
app_config = apps.get_app_config('api')

# Register all models
for model_name, model in app_config.models.items():
    admin.site.register(model)