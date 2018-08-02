import random
from django.core.management.base import BaseCommand
from puretask.models import Color, Car

MAX_PRICE = 1000000


class Command(BaseCommand):
    help = 'Upload data to Db for testing'

    def handle(self, *args, **options):
        colors = []
        for color in ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']:
            color_object = Color.objects.create(name=color)
            colors.append(color_object)
        for i in range(10):
            price = int(random.random()*MAX_PRICE)
            color = random.choice(colors)
            Car.objects.create(parameters={'price': price, 'colorId': color.id})

        self.stdout.write(self.style.SUCCESS('Initial data upladed'))
