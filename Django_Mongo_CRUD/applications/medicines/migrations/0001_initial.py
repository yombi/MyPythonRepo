# Generated by Django 3.2.9 on 2021-12-16 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('medicine_id', models.AutoField(primary_key=True, serialize=False)),
                ('common_name', models.CharField(max_length=100)),
                ('scientific_name', models.CharField(max_length=100)),
                ('available', models.CharField(max_length=2)),
                ('category', models.CharField(max_length=100)),
            ],
        ),
    ]
