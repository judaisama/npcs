# Generated by Django 2.2.6 on 2019-11-04 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0011_auto_20191101_0246'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpiderConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='爬虫名')),
                ('status', models.IntegerField(choices=[(1, '已开启'), (0, '已关闭')], default=0, verbose_name='用户情感')),
            ],
        ),
    ]
