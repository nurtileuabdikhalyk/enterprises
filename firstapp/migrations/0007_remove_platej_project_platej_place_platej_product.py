# Generated by Django 4.1 on 2023-02-14 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0006_remove_order_address_remove_order_oplata_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platej',
            name='project',
        ),
        migrations.AddField(
            model_name='platej',
            name='place',
            field=models.CharField(default=5, max_length=255, verbose_name='Орналасқан орны'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='platej',
            name='product',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='firstapp.product', verbose_name='Тауар'),
            preserve_default=False,
        ),
    ]
