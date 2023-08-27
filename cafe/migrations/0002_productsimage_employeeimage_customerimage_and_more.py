# Generated by Django 4.2.4 on 2023-08-27 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.product')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='employee_image')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.employee')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='customer_image')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.customer')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='category_image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.category')),
            ],
        ),
    ]
