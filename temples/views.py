from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg, Count

from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)
from django.contrib.auth import (
    login,
    authenticate,
    logout
)
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Temple, Review, Favorite
from .forms import TempleForm, ReviewForm
from .serializers import TempleSerializer


# ================= HOME =================

def home(request):

    top_temples = (
        Temple.objects.annotate(
            average_rating=Avg("reviews__rating"),
            review_count=Count("reviews")
        )
        .filter(review_count__gt=0)
        .order_by("-average_rating")[:6]
    )

    return render(
        request,
        "index.html",
        {
            "top_temples": top_temples
        }
    )


# ================= EXPLORE =================

def explore(request):

    temples = Temple.objects.all()

    return render(
        request,
        "explore.html",
        {
            "temples": temples
        }
    )


# ================= TEMPLE DETAILS =================

def temple(request, temple_id):

    temple = get_object_or_404(
        Temple,
        id=temple_id
    )

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.temple = temple

            review.save()

            messages.success(
                request,
                "Review added successfully!"
            )

            return redirect(
                "temple",
                temple_id=temple.id
            )

    else:

        form = ReviewForm()

    reviews = temple.reviews.all().order_by("-created_at")

    rating_data = temple.reviews.aggregate(
        average_rating=Avg("rating"),
        total_reviews=Count("id")
    )

    return render(
        request,
        "temple.html",
        {
            "temple": temple,
            "form": form,
            "reviews": reviews,
            "rating_data": rating_data,
        }
    )


# ================= ADD TEMPLE =================

@login_required
def add_temple(request):

    if request.method == "POST":

        form = TempleForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Temple added successfully!"
            )

            return redirect("explore")

    else:

        form = TempleForm()

    return render(
        request,
        "addtemple.html",
        {
            "form": form
        }
    )


# ================= ABOUT =================

def about(request):
    return render(request, "about.html")


# ================= REST API =================

@api_view(["GET"])
def temple_list_api(request):

    temples = Temple.objects.all()

    serializer = TempleSerializer(
        temples,
        many=True
    )

    return Response(serializer.data)


# ================= REGISTER =================

def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Registration successful!"
            )

            return redirect("home")

    else:

        form = UserCreationForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


# ================= LOGIN =================

def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    "Login successful!"
                )

                return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    else:

        form = AuthenticationForm()

    return render(
        request,
        "login.html",
        {
            "form": form
        }
    )


# ================= LOGOUT =================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("home")


# ================= ADD FAVORITE =================

@login_required
def add_favorite(request, temple_id):

    temple = get_object_or_404(
        Temple,
        id=temple_id
    )

    Favorite.objects.get_or_create(
        user=request.user,
        temple=temple
    )

    messages.success(
        request,
        "Temple added to favorites."
    )

    return redirect(
        "temple",
        temple_id=temple.id
    )


# ================= FAVORITES =================

@login_required
def favorites(request):

    favorites = Favorite.objects.filter(
        user=request.user
    )

    return render(
        request,
        "favorites.html",
        {
            "favorites": favorites
        }
    )