# Generated by Django 4.2.16 on 2025-03-18 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='attachement',
        ),
    ]
