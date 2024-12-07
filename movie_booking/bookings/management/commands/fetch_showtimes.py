import json
from django.core.management.base import BaseCommand
from bookings.models import Movie, Showtime

class Command(BaseCommand):
    help = 'Fetch showtimes from movies.json and populate the database'

    def handle(self, *args, **kwargs):
        json_file_path = "movies.json"  # Update this path if needed

        try:
            # Open and load the JSON file
            with open(json_file_path, "r") as file:
                movies_data = json.load(file)

            for movie_entry in movies_data:
                movie_title = movie_entry.get("title")
                if not movie_title:
                    self.stdout.write(self.style.WARNING("Skipping movie with missing title"))
                    continue

                genre = movie_entry.get("genre", "Unknown")
                duration = movie_entry.get("duration", 120)  # Default to 120 minutes
                rating = movie_entry.get("rating", 5.0)  # Default rating

                # Create or get the movie in the database
                movie, created = Movie.objects.get_or_create(
                    title=movie_title,
                    defaults={
                        "genre": genre,
                        "duration": duration,
                        "rating": rating,
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added movie: {movie_title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Movie already exists: {movie_title}"))

                # Add showtimes for the movie
                for showtime_entry in movie_entry.get("showtimes", []):
                    showtime_date = showtime_entry.get("date")
                    showtime_time = showtime_entry.get("time")
                    cinema_hall = showtime_entry.get("cinema_hall", "Unknown")

                    if not showtime_date or not showtime_time:
                        self.stdout.write(
                            self.style.WARNING(f"Skipping showtime for {movie_title} due to missing date or time")
                        )
                        continue

                    Showtime.objects.get_or_create(
                        movie=movie,
                        date=showtime_date,
                        time=showtime_time,
                        cinema_hall=cinema_hall,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Added showtime for {movie_title} at {cinema_hall} on {showtime_date} {showtime_time}"
                        )
                    )

            self.stdout.write(self.style.SUCCESS("Movies and showtimes fetch completed."))

        except FileNotFoundError:
            self.stderr.write(f"File not found: {json_file_path}")
        except json.JSONDecodeError:
            self.stderr.write("Error decoding JSON file.")
        except Exception as e:
            self.stderr.write(f"An error occurred: {str(e)}")

    def populate_movies_and_showtimes(data):
        for movie_data in data:
            movie, created = Movie.objects.get_or_create(
                title=movie_data.get("title", "Unknown Title"),
                defaults={
                    "genre": movie_data.get("genre", "Unknown Genre"),
                    "duration": movie_data.get("duration", 0),
                    "rating": movie_data.get("rating", 0.0),
                },
            )
            for showtime_data in movie_data.get("showtimes", []):
                Showtime.objects.get_or_create(
                    movie=movie,
                    date=showtime_data.get("date"),
                    time=showtime_data.get("time"),
                    cinema_hall=showtime_data.get("cinema_hall", "Unknown Hall"),
                )

