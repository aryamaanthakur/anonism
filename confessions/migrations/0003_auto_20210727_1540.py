# Generated by Django 3.2.5 on 2021-07-27 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('confessions', '0002_confession_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfessionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='confession',
            name='email',
        ),
    ]
