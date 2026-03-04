# Add more categories that anyone can understand (not only programmers)

from django.db import migrations


def add_friendly_categories(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    extra = [
        ("Getting Started", "First steps and basics"),
        ("Tips & Tricks", "Useful tips for everyone"),
        ("General", "General topics"),
        ("Questions", "Questions and answers"),
        ("Ideas", "Ideas and notes"),
    ]
    for name, desc in extra:
        Category.objects.get_or_create(name=name, defaults={"description": desc})


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_create_default_categories"),
    ]

    operations = [
        migrations.RunPython(add_friendly_categories, noop),
    ]
