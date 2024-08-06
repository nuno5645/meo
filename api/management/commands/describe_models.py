#describe_models.py

from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models

MAX_CHOICES = 10

class Command(BaseCommand):
    help = 'Print schema of specified models including field choices'

    def add_arguments(self, parser):
        parser.add_argument('names', nargs='*', type=str, help='List of model names or app names to process')
        parser.add_argument('--all', action='store_true', help='Process all models in all apps')

    def handle(self, *args, **options):
        names = options['names']
        process_all = options['all']

        if process_all:
            models_to_process = apps.get_models()
        elif not names:
            self.stdout.write(self.style.ERROR("Please specify model names, app names, or use --all"))
            return
        else:
            models_to_process = self.get_models_from_names(names)

        for model in models_to_process:
            self.print_model_schema(model)

    def get_models_from_names(self, names):
        models_to_process = []
        for name in names:
            if '.' in name:  # Assume it's a fully qualified model name
                try:
                    models_to_process.append(apps.get_model(name))
                except LookupError:
                    self.stdout.write(self.style.ERROR(f"Model '{name}' not found"))
            else:
                # Check if it's an app name
                try:
                    app_config = apps.get_app_config(name)
                    models_to_process.extend(app_config.get_models())
                except LookupError:
                    # If not an app, search for the model in all apps
                    found = False
                    for app_config in apps.get_app_configs():
                        try:
                            model = app_config.get_model(name)
                            models_to_process.append(model)
                            found = True
                            break
                        except LookupError:
                            continue
                    if not found:
                        self.stdout.write(self.style.ERROR(f"Model or app '{name}' not found"))
        return models_to_process

    def print_model_schema(self, model):
        self.stdout.write(self.style.SUCCESS(f"\nModel: {model.__name__}"))
        self.stdout.write("Fields:")

        for field in model._meta.fields:
            field_type = type(field).__name__
            field_info = f"  - {field.name} ({field_type})"

            if isinstance(field, models.ForeignKey):
                related_model = field.remote_field.model.__name__
                field_info += f" -> {related_model}"

            if hasattr(field, 'choices') and field.choices:
                choices = field.choices[:MAX_CHOICES]  # Get first MAX_CHOICES choices
                choices_str = ", ".join([f"{key}: {value}" for key, value in choices])
                
                if len(field.choices) > MAX_CHOICES:
                    remaining = len(field.choices) - MAX_CHOICES
                    choices_str += f", +{remaining} others"
                
                field_info += f"\n    Choices: {choices_str}"

            self.stdout.write(field_info)

        self.stdout.write("\n")