# Generated by Django 4.2.5 on 2024-11-21 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0018_alter_user_email_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.CharField(default='[avatars/(2).jpg]', max_length=255),
        ),
    ]
