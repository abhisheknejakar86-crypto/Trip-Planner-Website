from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from travel.models import BrowsingHistory, TripBooking

from .forms import RememberMeAuthenticationForm, SignUpForm


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. You can now keep your bookings and history private.")
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = RememberMeAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if form.cleaned_data.get("remember_me"):
                request.session.set_expiry(60 * 60 * 24 * 14)
            else:
                request.session.set_expiry(0)
            messages.success(request, "Welcome back. Your trip space is ready.")
            return redirect(request.GET.get("next") or "home")
    else:
        form = RememberMeAuthenticationForm(request)

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


@login_required
def history_view(request):
    bookings = (
        TripBooking.objects.filter(user=request.user)
        .select_related("destination", "hotel", "transport", "holiday_package")
        .order_by("-created_at")
    )
    browsed_items = BrowsingHistory.objects.filter(user=request.user).order_by("-viewed_at")[:30]
    return render(
        request,
        "accounts/history.html",
        {
            "bookings": bookings,
            "browsed_items": browsed_items,
        },
    )
