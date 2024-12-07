from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserChangeForm
from .models import Movie, Showtime, Booking
from .forms import BookingForm, LoginForm, CustomUserCreationForm, ShowtimeForm

from serpapi import GoogleSearch
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

from django.contrib.auth import get_user_model


def home(request):
    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['q']
            location = form.cleaned_data['location']
            
            # Fetch data from API using query and location
            params = {
                "q": query,
                "location": location,
                "hl": "en",
                "gl": "us",
                "api_key": "YOUR_SERPAPI_KEY"
            }
            search = GoogleSearch(params)
            result = search.get_dict()

            # Process the API response and update the database
            if "showtimes" in result:
                for showtime_data in result['showtimes']:
                    movie_title = query.lower()
                    movie, _ = Movie.objects.get_or_create(title=movie_title)

                    Showtime.objects.create(
                        movie=movie,
                        date=showtime_data.get('date', 'N/A'),
                        time=showtime_data.get('time', 'N/A'),
                        cinema_hall=showtime_data.get('cinema_hall', 'N/A')
                    )
            
            # Redirect to the movie list view
            return redirect('movie_list')
    else:
        form = MovieSearchForm()

    return render(request, 'home.html', {'form': form})

def movie_list(request):
    movies = Movie.objects.prefetch_related('showtimes').all()  # Use 'showtimes' instead of 'showtime_set'
    return render(request, 'movie_list.html', {'movies': movies})
# Movie Details
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie)
    return render(request, 'movie_detail.html', {'movie': movie, 'showtimes': showtimes})

@login_required
def add_showtime(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ShowtimeForm(request.POST)
        if form.is_valid():
            showtime = form.save(commit=False)
            showtime.movie = movie
            showtime.save()
            return redirect('movie_list')  # Redirect to the movie list
    else:
        form = ShowtimeForm()

    return render(request, 'book_showtime.html', {'form': form, 'movie': movie, 'form_mode': 'add'})

# Booking Page


@login_required
def book_showtime(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.showtime = showtime
            booking.total_cost = booking.tickets * 10.00
            booking.save()
            return redirect('booking_history')  # Redirect to the booking history
    else:
        form = BookingForm()

    return render(request, 'book_showtime.html', {'form': form, 'showtime': showtime, 'form_mode': 'book'})


def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).select_related("showtime", "showtime__movie")
    return render(request, "booking_history.html", {"bookings": bookings})

def delete_all_bookings(request):
    if request.method == "POST" and request.user.is_authenticated:
        # Delete all bookings for the authenticated user
        Booking.objects.filter(user=request.user).delete()
        return redirect('booking_history')
    return redirect('login')


@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})



def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('home')  # Redirect to the home page
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    #logout(request)
    return redirect('home')

def custom_logout(request):
    auth_logout(request)  # Use the Django's built-in logout
    return redirect('home') 

User = get_user_model()
# User Registration
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email address.')
                return render(request, 'bookings/login.html', {'form': form})

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid password. Please try again.')
        else:
            messages.error(request, 'Invalid input. Please check your credentials.')
    else:
        form = LoginForm()
    
    return render(request, 'bookings/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})