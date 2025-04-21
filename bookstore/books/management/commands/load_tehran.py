import json
from django.core.management.base import BaseCommand
from books.models import County
from django.contrib.gis.geos import GEOSGeometry

class Command(BaseCommand):
    help = "Load Tehran boundary from tehran.geojson"

    def handle(self, *args, **options):
        if County.objects.filter(name='تهران').exists():
            self.stdout.write(self.style.WARNING('Tehran already loaded. Skipping.'))
            return

        try:
            with open('data/tehran.geojson', encoding='utf-8') as f:
                data = json.load(f)

                for feature in data['features']:
                    geom = GEOSGeometry(json.dumps(feature['geometry']))
                    name = feature['properties'].get('name', 'تهران')

                    County.objects.create(name=name, geometry=geom)

                self.stdout.write(self.style.SUCCESS('Tehran GeoJSON loaded successfully.'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('GeoJSON file not found.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading GeoJSON: {e}'))
