# Generated by Django 4.2.10 on 2024-05-10 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_alter_problem_created_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Students',
        ),
    ]
