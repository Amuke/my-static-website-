# Generated by Django 3.2.25 on 2024-05-31 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20240531_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='color',
            field=models.CharField(default='#000000', max_length=7),
        ),
    ]