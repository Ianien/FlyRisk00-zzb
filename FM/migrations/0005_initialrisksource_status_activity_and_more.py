# Generated by Django 4.1.2 on 2023-04-10 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FM', '0004_risksource_by_subjectharm'),
    ]

    operations = [
        migrations.AddField(
            model_name='initialrisksource',
            name='status_activity',
            field=models.CharField(default='等待审核', max_length=20, null=True, verbose_name='当前问卷状态'),
        ),
        migrations.AddField(
            model_name='risksourceactivity',
            name='status_activity',
            field=models.CharField(default='问卷收集中', max_length=20, null=True, verbose_name='当前活动状态'),
        ),
    ]
