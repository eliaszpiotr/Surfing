# Generated by Django 4.1.7 on 2023-06-05 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0003_alter_userprofile_boards_alter_userprofile_friends_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surfboard',
            name='length',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='surfboard',
            name='thickness',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='surfboard',
            name='volume',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='surfboard',
            name='width',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
