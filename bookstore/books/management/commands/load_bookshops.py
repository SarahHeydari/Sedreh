import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from books.models import Bookshop

class Command(BaseCommand):
    help = 'Load bookshops from a GeoJSON file'

    def handle(self, *args, **kwargs):
        path = 'books/bookshops.geojson'

        with open(path, 'r') as file:
            data = json.load(file)

        count = 0
        for feature in data['features']:
            geometry = feature.get('geometry')
            if not geometry or geometry.get('type') != 'Point':
                continue

            coords = geometry.get('coordinates')
            if not coords or len(coords) != 2:
                continue

            lon, lat = coords
            try:
                location = Point(lon, lat)
            except Exception as e:
                continue

            name = feature['properties'].get('name', 'No Name')

            _, created = Bookshop.objects.get_or_create(name=name, location=location)
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} bookshops loaded successfully.'))
