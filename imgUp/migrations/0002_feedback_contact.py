# Generated by Django 3.0.3 on 2021-02-16 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgUp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='contact',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
