from django.db import migrations
from django.contrib.gis.db import models
import django.contrib.gis.db.models.fields

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_bookshop'),  # اینو بر اساس آخرین فایل قبلی تغییر بده
    ]

    operations = [
        migrations.RemoveField(
            model_name='county',
            name='area',
        ),
        migrations.AddField(
            model_name='county',
            name='geometry',
            field=django.contrib.gis.db.models.fields.PolygonField(geography=True, srid=4326, null=True),
        ),
    ]
