# Generated by Django 4.1.3 on 2023-01-05 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_student_encodings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='encodings',
            field=models.BinaryField(default=None, null=True),
        ),
    ]
