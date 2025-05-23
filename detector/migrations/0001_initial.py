# Generated by Django 5.2 on 2025-05-12 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DetectionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('files_detected', models.JSONField()),
                ('processes_detected', models.JSONField()),
                ('scan_duration', models.FloatField()),
                ('system_info', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('path', models.CharField(max_length=255)),
                ('is_new', models.BooleanField(default=True)),
            ],
            options={
                'indexes': [models.Index(fields=['timestamp'], name='detector_vi_timesta_0e8213_idx'), models.Index(fields=['ip_address'], name='detector_vi_ip_addr_127c3a_idx')],
            },
        ),
    ]
