# Generated by Django 4.2.5 on 2024-10-12 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_user_profile_pic_alter_user_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.CharField(default='avatars/(1).jpg', max_length=255),
        ),
    ]