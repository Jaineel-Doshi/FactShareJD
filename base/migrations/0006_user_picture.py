# Generated by Django 4.0.4 on 2022-08-18 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.CharField(blank=True, default='5', editable=False, max_length=10, null=True),
        ),
    ]