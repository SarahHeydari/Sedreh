# accounts/migrations/0002_initial.py
from django.db import migrations
from django.contrib.gis.db import models



class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='CustomUser',
            name='location',
            field=models.PointField(geography=True)

        ),
    ]
