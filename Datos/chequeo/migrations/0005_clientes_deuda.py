# Generated by Django 3.0.8 on 2020-07-28 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chequeo', '0004_clientes_dias'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='deuda',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
