# Generated by Django 4.1.2 on 2023-04-21 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FM', '0011_initialsubjectharm_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='initialsubjectharm',
            name='risk_level',
        ),
        migrations.AddField(
            model_name='initialsubjectharm',
            name='R_value',
            field=models.CharField(default=1, max_length=32, verbose_name='危害评分'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='initialsubjectharm',
            name='harm_level',
            field=models.CharField(default=1, max_length=32, verbose_name='危害等级'),
            preserve_default=False,
        ),
    ]
