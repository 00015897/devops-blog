# Data migration: create default categories so "Create Post" has options

from django.db import migrations


def create_default_categories(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    defaults = [
        ("DevOps", "DevOps and automation"),
        ("Django", "Django framework"),
        ("Docker", "Containerization"),
    ]
    for name, desc in defaults:
        Category.objects.get_or_create(name=name, defaults={"description": desc})


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_categories, noop),
    ]
