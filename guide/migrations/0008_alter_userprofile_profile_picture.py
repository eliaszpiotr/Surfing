# Generated by Django 4.1.7 on 2023-06-06 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guide', '0007_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='profile_pictures/def.jpeg', upload_to='profile_pictures'),
        ),
    ]
