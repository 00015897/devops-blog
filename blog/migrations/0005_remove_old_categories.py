# Remove old categories so only coffee shop topics remain

from django.db import migrations


def remove_old_categories(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    old_names = [
        "DevOps",
        "Django",
        "Docker",
        "Getting Started",
        "Tips & Tricks",
        "General",
        "Questions",
        "Ideas",
    ]
    Category.objects.filter(name__in=old_names).delete()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_add_coffee_shop_categories"),
    ]

    operations = [
        migrations.RunPython(remove_old_categories, noop),
    ]
