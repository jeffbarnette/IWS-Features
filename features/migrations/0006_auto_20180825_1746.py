# Generated by Django 2.1 on 2018-08-25 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0005_auto_20180825_0548'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ('client_name',)},
        ),
        migrations.AlterModelOptions(
            name='feature',
            options={'ordering': ('client', 'client_priority')},
        ),
        migrations.AlterModelOptions(
            name='prodarea',
            options={'ordering': ('prod_area',)},
        ),
        migrations.AlterField(
            model_name='client',
            name='client_name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='feature',
            name='client_priority',
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True),
        ),
    ]
