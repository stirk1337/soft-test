import asyncio

from django.core.management.base import BaseCommand

from app.internal.parser import AsyncHabrParser


class Command(BaseCommand):
    help = 'Habr parser start'

    def handle(self, *args, **options) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        parser = AsyncHabrParser()
        loop.run_until_complete(parser.start_parser())
        loop.close()
