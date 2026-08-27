from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date

from django.db.models import Min, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TripBookingForm, TripSearchForm
from .models import BrowsingHistory, Destination, HolidayPackage, Hotel, TransportOption


SERVICE_TABS = [
    {"key": "flights", "label": "Flights", "icon": "plane", "kind": "transport", "transport_type": TransportOption.PLANE},
    {"key": "hotels", "label": "Hotels", "icon": "hotel", "kind": "hotel"},
    {"key": "villas", "label": "Villas & Homestays", "icon": "villa", "kind": "hotel"},
    {"key": "packages", "label": "Holiday Packages", "icon": "package", "kind": "package"},
    {"key": "trains", "label": "Trains", "icon": "train", "kind": "transport", "transport_type": TransportOption.TRAIN},
    {"key": "buses", "label": "Buses", "icon": "bus", "kind": "transport", "transport_type": TransportOption.BUS},
    {"key": "cabs", "label": "Cabs", "icon": "cab", "kind": "transport", "transport_type": TransportOption.CAB},
    {"key": "tours", "label": "Tours & Attractions", "icon": "tour", "kind": "package"},
    {"key": "cruise", "label": "Cruise", "icon": "cruise", "kind": "package"},
]

SERVICE_PROMOS = {
    "flights": [
        ("Cheapest fare finder", "Compare multiple airlines with direct and one-stop options."),
        ("Non-stop first", "Spot faster routes and best departure windows quickly."),
        ("Bank and wallet offers", "Apply seasonal discounts on selected flight partners."),
    ],
    "hotels": [
        ("Premium stays", "Handpicked hotels with strong ratings and breakfast options."),
        ("Most preferred", "See properties near beaches, airports, stations, and city centers."),
        ("Pay later choices", "Shortlist stays and request booking confirmation later."),
    ],
    "villas": [
        ("Private stays", "Find villas, cottages, homestays, and serviced apartments."),
        ("Group friendly", "Better spaces for families, teams, and long weekend plans."),
        ("Kitchen and lounge", "Filter for spacious stays with home-style amenities."),
    ],
    "packages": [
        ("Bundled savings", "Hotels, transfers, sightseeing, and guided plans together."),
        ("International holidays", "Explore Dubai, Singapore, Bali, Paris, London, and Maldives."),
        ("Flexible itineraries", "Pick compact weekends or longer premium vacations."),
    ],
    "trains": [
        ("Fast rail options", "Compare early morning, evening, and overnight departures."),
        ("Station-friendly", "Plan city-to-city trips with convenient arrival times."),
        ("Budget routes", "Find economical routes for reliable domestic travel."),
    ],
    "buses": [
        ("Volvo and sleeper", "Compare overnight coaches, AC buses, and express operators."),
        ("Live seat availability", "Check routes with seats left for popular weekend trips."),
        ("Low fare routes", "Great for regional travel and short breaks."),
    ],
    "cabs": [
        ("Doorstep pickup", "Book airport drops, hill routes, and intercity transfers."),
        ("Private ride comfort", "Best for families, local sightseeing, and flexible stops."),
        ("Transparent pricing", "Compare providers by route, seats, and fare."),
    ],
    "tours": [
        ("Local experiences", "Add guided walks, food trails, adventure activities, and city tours."),
        ("Curated highlights", "See the best-rated attractions for every destination."),
        ("Short plans", "Perfect for travellers with limited time in a city."),
    ],
    "cruise": [
        ("Island routes", "Explore coastal, island, and premium cruise-style holidays."),
        ("Resort pairing", "Combine water transfers with beach hotels and packages."),
        ("Leisure first", "Slower, scenic itineraries for relaxed holidays."),
    ],
}

CITY_SUGGESTIONS = [
    "New Delhi",
    "Bengaluru",
    "Mumbai",
    "Goa",
    "Dubai",
    "Singapore",
    "Bali",
    "London",
    "Paris",
    "Maldives",
    "Jaipur",
    "Agra",
    "Kerala",
    "Rishikesh",
    "Darjeeling",
    "Andaman",
]

STAY_SUGGESTIONS = [
    "Goa",
    "Bengaluru",
    "Mumbai",
    "Dubai",
    "Singapore",
    "Bali",
    "London",
    "Paris",
    "Maldives",
    "Jaipur",
    "Kerala",
    "Andaman",
    "Udaipur",
    "Rishikesh",
]

ROUTE_SUGGESTIONS = [
    "New Delhi",
    "Bengaluru",
    "Mumbai",
    "Chennai",
    "Kolkata",
    "Ahmedabad",
    "Kochi",
    "Goa",
    "Jaipur",
    "Agra",
    "Dubai",
    "Singapore",
    "Bali",
    "London",
    "Paris",
    "Maldives",
]

SERVICE_MODES = {
    "hotels": "stay",
    "villas": "stay",
    "packages": "destination",
    "tours": "destination",
    "cruise": "destination",
}


def get_service_tab(service):
    return next((item for item in SERVICE_TABS if item["key"] == service), SERVICE_TABS[0])


def record_browsing(request, item_type, item_name, destination_name="", price=None, image_url="", notes=""):
    if request.user.is_authenticated:
        BrowsingHistory.objects.create(
            user=request.user,
            item_type=item_type,
            item_name=item_name,
            destination_name=destination_name,
            price=price,
            image_url=image_url,
            notes=notes,
        )


def home(request):
    form = TripSearchForm(request.GET or None)
    destinations = Destination.objects.all()
    hotels = Hotel.objects.select_related("destination")
    transports = TransportOption.objects.select_related("destination")
    packages = HolidayPackage.objects.select_related("destination")

    if form.is_valid():
        query = form.cleaned_data.get("destination")
        travel_type = form.cleaned_data.get("travel_type")
        max_budget = form.cleaned_data.get("max_budget")

        if query:
            destinations = destinations.filter(
                Q(name__icontains=query) | Q(country__icontains=query) | Q(description__icontains=query)
            )
            hotels = hotels.filter(
                Q(name__icontains=query)
                | Q(destination__name__icontains=query)
                | Q(destination__country__icontains=query)
            )
            packages = packages.filter(
                Q(title__icontains=query)
                | Q(destination__name__icontains=query)
                | Q(destination__country__icontains=query)
            )
            transports = transports.filter(
                Q(source__icontains=query)
                | Q(destination__name__icontains=query)
                | Q(destination__country__icontains=query)
                | Q(provider_name__icontains=query)
            )

        if travel_type:
            transports = transports.filter(transport_type=travel_type)

        if max_budget is not None:
            hotels = hotels.filter(price_per_night__lte=max_budget)
            transports = transports.filter(price__lte=max_budget)
            packages = packages.filter(price_per_person__lte=max_budget)

    context = {
        "form": form,
        "service_tabs": SERVICE_TABS,
        "service_promos": SERVICE_PROMOS,
        "city_suggestions": CITY_SUGGESTIONS,
        "route_suggestions": ROUTE_SUGGESTIONS,
        "stay_suggestions": STAY_SUGGESTIONS,
        "service_modes": SERVICE_MODES,
        "today": date.today().isoformat(),
        "hotel_count": Hotel.objects.count(),
        "transport_count": TransportOption.objects.count(),
        "package_count": HolidayPackage.objects.count(),
        "destinations": destinations[:9],
        "hotels": hotels[:6],
        "transports": transports[:6],
        "packages": packages[:6],
    }
    return render(request, "travel/home.html", context)


def service_search(request, service):
    active_tab = get_service_tab(service)
    from_city = request.GET.get("from", "").strip()
    to_city = request.GET.get("to", "").strip()
    location = request.GET.get("location", "").strip()
    depart = request.GET.get("depart", "").strip()
    return_date = request.GET.get("return", "").strip()
    travellers = request.GET.get("travellers", "1").strip() or "1"
    travel_class = request.GET.get("travel_class", "Economy").strip() or "Economy"
    max_price = request.GET.get("max_price", "").strip()
    provider = request.GET.get("provider", "").strip()
    sort = request.GET.get("sort", "price").strip()

    results = []
    price_min = None
    price_max = None

    search_place = location or to_city

    if active_tab["kind"] == "transport":
        queryset = TransportOption.objects.select_related("destination").filter(
            transport_type=active_tab["transport_type"]
        )
        if from_city:
            queryset = queryset.filter(source__icontains=from_city)
        if to_city:
            queryset = queryset.filter(
                Q(destination__name__icontains=to_city) | Q(destination__country__icontains=to_city)
            )
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if provider:
            queryset = queryset.filter(provider_name__icontains=provider)
        if sort == "time":
            queryset = queryset.order_by("departure_time")
        else:
            queryset = queryset.order_by("price")
        price_min = queryset.aggregate(Min("price"))["price__min"]
        results = queryset

    elif active_tab["kind"] == "hotel":
        queryset = Hotel.objects.select_related("destination")
        if search_place:
            queryset = queryset.filter(
                Q(destination__name__icontains=search_place)
                | Q(destination__country__icontains=search_place)
                | Q(name__icontains=search_place)
            )
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)
        queryset = queryset.order_by("price_per_night" if sort == "price" else "-star_rating")
        price_min = queryset.aggregate(Min("price_per_night"))["price_per_night__min"]
        results = queryset

    elif active_tab["kind"] == "package":
        queryset = HolidayPackage.objects.select_related("destination")
        if search_place:
            queryset = queryset.filter(
                Q(destination__name__icontains=search_place)
                | Q(destination__country__icontains=search_place)
                | Q(title__icontains=search_place)
            )
        if max_price:
            queryset = queryset.filter(price_per_person__lte=max_price)
        queryset = queryset.order_by("price_per_person" if sort == "price" else "duration_days")
        price_min = queryset.aggregate(Min("price_per_person"))["price_per_person__min"]
        results = queryset

    else:
        results = []

    price_values = []
    for item in results:
        if active_tab["kind"] == "transport":
            price_values.append(item.price)
        elif active_tab["kind"] == "hotel":
            price_values.append(item.price_per_night)
        elif active_tab["kind"] == "package":
            price_values.append(item.price_per_person)
    if price_values:
        price_max = max(price_values)

    context = {
        "service_tabs": SERVICE_TABS,
        "service_promos": SERVICE_PROMOS,
        "city_suggestions": CITY_SUGGESTIONS,
        "route_suggestions": ROUTE_SUGGESTIONS,
        "stay_suggestions": STAY_SUGGESTIONS,
        "service_modes": SERVICE_MODES,
        "active_tab": active_tab,
        "results": results,
        "from_city": from_city or "New Delhi",
        "to_city": to_city or location or "Bengaluru",
        "location": location or to_city or "Goa",
        "depart": depart,
        "return_date": return_date,
        "travellers": travellers,
        "travel_class": travel_class,
        "price_min": price_min,
        "price_max": price_max,
        "selected_sort": sort,
        "max_price": max_price,
        "selected_provider": provider,
        "provider_options": (
            TransportOption.objects.filter(transport_type=active_tab.get("transport_type"))
            .values_list("provider_name", flat=True)
            .distinct()
            if active_tab["kind"] == "transport"
            else []
        ),
        "today": date.today().isoformat(),
    }
    return render(request, "travel/search_results.html", context)


def hotels(request):
    hotel_list = Hotel.objects.select_related("destination")
    return render(request, "travel/hotels.html", {"hotels": hotel_list})


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel.objects.select_related("destination"), pk=pk)
    record_browsing(
        request,
        BrowsingHistory.HOTEL,
        hotel.name,
        hotel.destination.name,
        hotel.price_per_night,
        hotel.image_url,
        f"{hotel.star_rating} star hotel",
    )
    return render(request, "travel/hotel_detail.html", {"hotel": hotel})


def transport(request):
    transport_list = TransportOption.objects.select_related("destination")
    return render(request, "travel/transport.html", {"transports": transport_list})


def transport_detail(request, pk):
    transport_option = get_object_or_404(TransportOption.objects.select_related("destination"), pk=pk)
    record_browsing(
        request,
        BrowsingHistory.TRANSPORT,
        transport_option.provider_name,
        transport_option.destination.name,
        transport_option.price,
        "",
        f"{transport_option.get_transport_type_display()} from {transport_option.source}",
    )
    return render(request, "travel/transport_detail.html", {"transport": transport_option})


def packages(request):
    package_list = HolidayPackage.objects.select_related("destination")
    return render(request, "travel/packages.html", {"packages": package_list})


def package_detail(request, pk):
    package = get_object_or_404(HolidayPackage.objects.select_related("destination"), pk=pk)
    record_browsing(
        request,
        BrowsingHistory.PACKAGE,
        package.title,
        package.destination.name,
        package.price_per_person,
        package.image_url,
        f"{package.duration_days} day package",
    )
    return render(request, "travel/package_detail.html", {"package": package})


def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    record_browsing(
        request,
        BrowsingHistory.DESTINATION,
        destination.name,
        destination.name,
        None,
        destination.image_url,
        destination.best_season,
    )
    return render(
        request,
        "travel/destination_detail.html",
        {
            "destination": destination,
            "hotels": destination.hotels.all()[:4],
            "transports": destination.transport_options.all()[:4],
            "packages": destination.packages.all()[:4],
        },
    )


@login_required
def book_trip(request):
    if request.method == "POST":
        form = TripBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, "Your trip request has been submitted. Our team will contact you soon.")
            return redirect("booking_success")
    else:
        initial = {
            "customer_name": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
        }
        form = TripBookingForm(initial=initial)

    return render(request, "travel/book_trip.html", {"form": form})


def booking_success(request):
    return render(request, "travel/booking_success.html")
