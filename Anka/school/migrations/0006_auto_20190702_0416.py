# Generated by Django 2.2.3 on 2019-07-02 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_auto_20190702_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
