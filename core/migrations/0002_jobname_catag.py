# Generated by Django 3.2 on 2022-01-03 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobname',
            name='catag',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.jobcatag'),
            preserve_default=False,
        ),
    ]
