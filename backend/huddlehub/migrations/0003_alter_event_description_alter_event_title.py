# Generated by Django 5.1.1 on 2024-10-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('huddlehub', '0002_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=256),
        ),
    ]
