# Generated by Django 3.2.4 on 2021-07-16 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20210716_0327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['date_posted']},
        ),
    ]