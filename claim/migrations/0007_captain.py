# Generated by Django 3.0.5 on 2020-06-21 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('claim', '0006_auto_20200621_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Captain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='claim.Group', to_field='group_name')),
                ('kv_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='claim.KV', to_field='KV_name')),
            ],
        ),
    ]
