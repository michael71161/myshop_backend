# Generated by Django 4.2.2 on 2023-06-30 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('desc', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.DecimalField(decimal_places=0, default=0, max_digits=4)),
                ('image', models.ImageField(blank=True, default='/placeholder.png', null=True, upload_to='Posted_Images')),
                ('createdTime', models.DateTimeField(auto_now_add=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.category')),
            ],
        ),
    ]
