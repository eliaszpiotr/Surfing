# Generated by Django 4.1.7 on 2023-06-05 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0005_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/default.jpg', null=True, upload_to='profile_pictures'),
        ),
    ]