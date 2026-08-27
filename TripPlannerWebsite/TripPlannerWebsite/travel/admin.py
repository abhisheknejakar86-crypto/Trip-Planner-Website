from django.contrib import admin

from .models import BrowsingHistory, Destination, HolidayPackage, Hotel, TransportOption, TripBooking


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "best_season")
    search_fields = ("name", "country")


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "destination", "star_rating", "price_per_night", "rooms_available")
    list_filter = ("star_rating", "destination")
    search_fields = ("name", "address")


@admin.register(TransportOption)
class TransportOptionAdmin(admin.ModelAdmin):
    list_display = (
        "provider_name",
        "transport_type",
        "source",
        "destination",
        "departure_time",
        "price",
        "seats_available",
    )
    list_filter = ("transport_type", "destination")
    search_fields = ("provider_name", "source")


@admin.register(HolidayPackage)
class HolidayPackageAdmin(admin.ModelAdmin):
    list_display = ("title", "destination", "duration_days", "price_per_person")
    list_filter = ("destination", "includes_hotel", "includes_transport")
    search_fields = ("title", "itinerary")


@admin.register(TripBooking)
class TripBookingAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "user", "booking_type", "destination", "travelers", "created_at")
    list_filter = ("booking_type", "destination", "created_at")
    search_fields = ("customer_name", "email", "phone", "user__username")
    readonly_fields = ("created_at",)


@admin.register(BrowsingHistory)
class BrowsingHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "item_type", "item_name", "destination_name", "price", "viewed_at")
    list_filter = ("item_type", "viewed_at")
    search_fields = ("user__username", "item_name", "destination_name")
    readonly_fields = ("viewed_at",)
