# Generated by Django 3.1.4 on 2020-12-19 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_aplicacion', '0003_auto_20201217_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='portada',
            field=models.ImageField(default='covers/default-cover.jpg', upload_to='covers'),
        ),
    ]