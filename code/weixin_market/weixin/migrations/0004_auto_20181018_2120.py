# Generated by Django 2.1 on 2018-10-18 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0003_auto_20180925_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='class_info',
            name='platform_name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='class_info',
            name='class_name',
            field=models.CharField(max_length=1000),
        ),
    ]