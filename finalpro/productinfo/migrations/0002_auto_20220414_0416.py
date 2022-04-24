# Generated by Django 3.2.12 on 2022-04-14 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productinfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['category_name']},
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('category_name',), name='unique_category'),
        ),
    ]