# Generated by Django 3.0.4 on 2020-05-22 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20200522_1606'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scrap',
            old_name='link',
            new_name='otherlink',
        ),
        migrations.AddField(
            model_name='game',
            name='link',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
