from django.core.management.base import BaseCommand
from django.db.models import Count
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from puretask.models import Car


class Command(BaseCommand):
    help = 'Group by and count cars by color'

    def handle(self, *args, **options):
        color_id = KeyTextTransform('colorId', 'parameters')
        cars = Car.objects\
            .annotate(color_id=color_id)\
            .values('color_id')\
            .annotate(Count('id'))\
            .order_by()
        for car in cars:
            self.stdout.write(self.style.SUCCESS(repr(car)))
