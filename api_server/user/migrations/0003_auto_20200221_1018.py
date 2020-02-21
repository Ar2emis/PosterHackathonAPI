# Generated by Django 3.0.3 on 2020-02-21 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_testmodel_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSubModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='testmodel',
            name='submodel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.TestSubModel'),
        ),
    ]
