# Generated by Django 3.1.7 on 2021-04-08 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20210406_1010'),
        ('projects', '0014_auto_20210408_1410'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projectmembershiprequest',
            unique_together={('from_user', 'to_project')},
        ),
    ]