# Generated by Django 4.2.5 on 2024-11-21 05:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_alter_user_profile_pic_userrecoverycode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.CharField(default='[avatars/(5).jpg]', max_length=255),
        ),
        migrations.AlterField(
            model_name='userrecoverycode',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recovery_codes', to=settings.AUTH_USER_MODEL),
        ),
    ]
