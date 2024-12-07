import json
from django.core.management.base import BaseCommand
from bookings.models import Movie, Showtime

class Command(BaseCommand):
    help = 'Populates the database with sample data from JSON'

    def handle(self, *args, **kwargs):
        try:
            with open('movies.json') as f:
                data = json.load(f)

            for item in data:
                movie_data = item["movie"]
                movie, created = Movie.objects.get_or_create(
                    title=movie_data["title"],
                    defaults={
                        "genre": movie_data.get("genre", "Unknown"),
                        "duration": movie_data.get("duration", 0),
                        "rating": movie_data.get("rating", 0.0)
                    }
                )

                for showtime in item["showtimes"]:
                    Showtime.objects.get_or_create(
                        movie=movie,
                        date=showtime["date"],
                        time=showtime["time"],
                        cinema_hall=showtime["cinema_hall"]
                    )

            self.stdout.write(self.style.SUCCESS("Sample data populated successfully!"))

        except Exception as e:
            self.stderr.write(f"An error occurred: {e}")
