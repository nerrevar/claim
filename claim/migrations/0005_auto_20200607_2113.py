# Generated by Django 3.0.5 on 2020-06-07 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0004_kv_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='error_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]