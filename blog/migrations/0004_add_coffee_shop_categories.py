# Categories for a coffee shop blog – users can write posts about these topics

from django.db import migrations


def add_coffee_shop_categories(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    categories = [
        ("Coffee", "Coffee drinks, beans, and brewing"),
        ("Menu", "Food and drinks we offer"),
        ("Reviews", "Reviews and recommendations"),
        ("Events", "Events, live music, meetups"),
        ("Atmosphere", "Our place, vibe, and space"),
        ("Tips", "Tips for coffee lovers"),
    ]
    for name, desc in categories:
        Category.objects.get_or_create(name=name, defaults={"description": desc})


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_add_friendly_categories"),
    ]

    operations = [
        migrations.RunPython(add_coffee_shop_categories, noop),
    ]
