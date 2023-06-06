# Generated by Django 4.1 on 2023-01-25 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0003_alter_platej_options_alter_platej_ndc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platej',
            name='ndc',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='НДС'),
        ),
        migrations.AlterField(
            model_name='platej',
            name='sum',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Сумма'),
        ),
    ]
