# Generated by Django 5.2.1 on 2025-05-31 21:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_subject_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='backend.subjectarea', verbose_name='Area'),
        ),
    ]
