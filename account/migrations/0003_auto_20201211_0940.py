# Generated by Django 3.1.4 on 2020-12-11 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_contact'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ('-created',)},
        ),
    ]
