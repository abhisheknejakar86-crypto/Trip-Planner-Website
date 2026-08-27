from django.db import models
from django.contrib.auth.models import User


class Destination(models.Model):
    name = models.CharField(max_length=120)
    country = models.CharField(max_length=80, default="India")
    description = models.TextField()
    image_url = models.URLField(blank=True)
    best_season = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}, {self.country}"


class Hotel(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="hotels")
    name = models.CharField(max_length=140)
    address = models.CharField(max_length=220)
    star_rating = models.PositiveSmallIntegerField(default=3)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    rooms_available = models.PositiveIntegerField(default=10)
    amenities = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ["price_per_night", "name"]

    def __str__(self):
        return self.name


class TransportOption(models.Model):
    PLANE = "plane"
    TRAIN = "train"
    BUS = "bus"
    CAB = "cab"

    TRANSPORT_CHOICES = [
        (PLANE, "Plane"),
        (TRAIN, "Train"),
        (BUS, "Bus"),
        (CAB, "Cab"),
    ]

    source = models.CharField(max_length=120)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="transport_options")
    transport_type = models.CharField(max_length=20, choices=TRANSPORT_CHOICES)
    provider_name = models.CharField(max_length=120)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seats_available = models.PositiveIntegerField(default=30)

    class Meta:
        ordering = ["price", "departure_time"]

    def __str__(self):
        return f"{self.get_transport_type_display()} by {self.provider_name}"


class HolidayPackage(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="packages")
    title = models.CharField(max_length=150)
    duration_days = models.PositiveSmallIntegerField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    includes_hotel = models.BooleanField(default=True)
    includes_transport = models.BooleanField(default=True)
    itinerary = models.TextField()
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ["price_per_person", "duration_days"]

    def __str__(self):
        return self.title


class TripBooking(models.Model):
    HOTEL = "hotel"
    TRANSPORT = "transport"
    PACKAGE = "package"

    BOOKING_CHOICES = [
        (HOTEL, "Hotel"),
        (TRANSPORT, "Transport"),
        (PACKAGE, "Holiday Package"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trip_bookings", null=True, blank=True)
    customer_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    booking_type = models.CharField(max_length=20, choices=BOOKING_CHOICES)
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    transport = models.ForeignKey(TransportOption, on_delete=models.SET_NULL, null=True, blank=True)
    holiday_package = models.ForeignKey(HolidayPackage, on_delete=models.SET_NULL, null=True, blank=True)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    travel_date = models.DateField(null=True, blank=True)
    travelers = models.PositiveSmallIntegerField(default=1)
    special_request = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name} - {self.get_booking_type_display()}"


class BrowsingHistory(models.Model):
    DESTINATION = "destination"
    HOTEL = "hotel"
    TRANSPORT = "transport"
    PACKAGE = "package"

    ITEM_CHOICES = [
        (DESTINATION, "Destination"),
        (HOTEL, "Hotel"),
        (TRANSPORT, "Transport"),
        (PACKAGE, "Holiday Package"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="browsing_history")
    item_type = models.CharField(max_length=20, choices=ITEM_CHOICES)
    item_name = models.CharField(max_length=160)
    destination_name = models.CharField(max_length=120, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(blank=True)
    notes = models.CharField(max_length=255, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-viewed_at"]
        verbose_name_plural = "browsing history"

    def __str__(self):
        return f"{self.user.username} viewed {self.item_name}"
