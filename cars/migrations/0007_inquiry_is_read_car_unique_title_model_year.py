# Generated manually for admin panel

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_car_model_year_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
