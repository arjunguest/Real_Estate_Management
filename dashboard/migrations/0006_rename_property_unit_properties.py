# Generated by Django 5.0 on 2024-01-17 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_property_post_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='unit',
            old_name='property',
            new_name='properties',
        ),
    ]
