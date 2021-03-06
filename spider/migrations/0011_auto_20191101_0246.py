# Generated by Django 2.2.6 on 2019-10-31 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0010_auto_20191101_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='jdgoods',
            name='comment_default_num',
            field=models.IntegerField(default=1, verbose_name='默认好评数'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jdgoods',
            name='goodrate',
            field=models.CharField(default=1, max_length=128, verbose_name='好评率'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jdgoods',
            name='score1_num',
            field=models.IntegerField(default=1, verbose_name='1星评价数'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jdgoods',
            name='score2_num',
            field=models.IntegerField(default=1, verbose_name='2星评价数'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jdgoods',
            name='score3_num',
            field=models.IntegerField(default=1, verbose_name='3星评价数'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jdgoods',
            name='score4_num',
            field=models.IntegerField(default=1, verbose_name='4星评价数'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jdgoods',
            name='score5_num',
            field=models.IntegerField(default=1, verbose_name='5星评价数'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jdgoods',
            name='comment_num',
            field=models.IntegerField(verbose_name='总评价数'),
        ),
    ]
