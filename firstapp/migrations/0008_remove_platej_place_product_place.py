# Generated by Django 4.1 on 2023-02-14 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0007_remove_platej_project_platej_place_platej_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platej',
            name='place',
        ),
        migrations.AddField(
            model_name='product',
            name='place',
            field=models.CharField(default=1, max_length=255, verbose_name='Орналасқан орны'),
            preserve_default=False,
        ),
    ]
