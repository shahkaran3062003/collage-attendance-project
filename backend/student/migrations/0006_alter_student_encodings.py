# Generated by Django 4.1.3 on 2023-02-21 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_alter_student_encodings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='encodings',
            field=models.CharField(default=None, max_length=5000, null=True),
        ),
    ]
