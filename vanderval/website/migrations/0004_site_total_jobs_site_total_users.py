# Generated by Django 5.1 on 2024-12-23 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_job_id_alter_site_id_alter_userrecords_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='total_jobs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='site',
            name='total_users',
            field=models.IntegerField(default=0),
        ),
    ]