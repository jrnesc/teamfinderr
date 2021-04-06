# Generated by Django 3.1.7 on 2021-04-06 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20210406_1010'),
        ('projects', '0004_auto_20210406_1346'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Membership',
            new_name='ProjectMembership',
        ),
        migrations.CreateModel(
            name='ProjectMembershipRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='profiles.userprofile')),
                ('to_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='projects.project')),
            ],
        ),
    ]
