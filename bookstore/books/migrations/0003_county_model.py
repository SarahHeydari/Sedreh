from django.db import migrations
from django.contrib.gis.db import models

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('area', models.PolygonField(geography=True)),
            ],
        ),
    ]
