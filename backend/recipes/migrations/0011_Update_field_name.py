# Generated by Django 3.2 on 2023-07-16 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_Update_related_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipeingredient',
            old_name='ingredients',
            new_name='ingredient',
        ),
    ]
