# Generated by Django 2.2.9 on 2020-05-20 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200520_1826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='group_name',
        ),
        migrations.AddField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
