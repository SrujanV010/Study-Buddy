# Generated by Django 4.2.7 on 2023-12-17 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_user_bio_user_name_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='static\\images\x07vatar.svg', null=True, upload_to=''),
        ),
    ]
