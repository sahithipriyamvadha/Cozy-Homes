# Generated by Django 4.1.5 on 2024-05-29 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_app', '0002_housedetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('username', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=60)),
            ],
        ),
    ]
