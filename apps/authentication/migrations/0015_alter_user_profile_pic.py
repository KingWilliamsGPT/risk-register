# Generated by Django 4.2.5 on 2024-11-14 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_activity_is_read_alter_activity_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.CharField(default='[avatars/(7).jpg]', max_length=255),
        ),
    ]