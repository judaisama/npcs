# Generated by Django 2.2.6 on 2019-10-23 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20191023_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='用户名'),
        ),
    ]
