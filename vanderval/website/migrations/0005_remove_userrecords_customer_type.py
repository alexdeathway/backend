# Generated by Django 5.1 on 2024-12-23 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_site_total_jobs_site_total_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrecords',
            name='customer_type',
        ),
    ]
