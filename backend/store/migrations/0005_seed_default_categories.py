from django.db import migrations


def seed_default_categories(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    default_categories = [
        'Food',
        'Rice',
        'Feeds',
        'Essential',
        'Drinks',
        'Pet Food',
    ]
    for name in default_categories:
        Category.objects.get_or_create(name=name)


def remove_seeded_categories(apps, schema_editor):
    Category = apps.get_model('store', 'Category')
    Category.objects.filter(name__in=[
        'Food', 'Rice', 'Feeds', 'Essential', 'Drinks', 'Pet Food'
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_cost_per_kilo_product_cost_per_sack'),
    ]

    operations = [
        migrations.RunPython(seed_default_categories, remove_seeded_categories),
    ]
