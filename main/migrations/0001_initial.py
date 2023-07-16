# Generated by Django 4.1.7 on 2023-03-08 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('regNum', models.CharField(max_length=100)),
                ('course', models.CharField(max_length=100)),
                ('branch', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
            ],
        ),
    ]