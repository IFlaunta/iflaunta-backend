# Generated by Django 3.2.6 on 2021-09-01 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0003_pastperformance'),
    ]

    operations = [
        migrations.CreateModel(
            name='PastPerformanceVideo',
            fields=[
                ('video_id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='')),
                ('performance_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pastPerformanceVideo', to='performance.pastperformance')),
            ],
        ),
    ]
