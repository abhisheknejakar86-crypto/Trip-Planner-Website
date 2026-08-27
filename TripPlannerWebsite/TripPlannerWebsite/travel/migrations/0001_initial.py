# Generated for the TripPlannerWebsite teaching project.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Destination",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("country", models.CharField(default="India", max_length=80)),
                ("description", models.TextField()),
                ("image_url", models.URLField(blank=True)),
                ("best_season", models.CharField(blank=True, max_length=120)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="HolidayPackage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150)),
                ("duration_days", models.PositiveSmallIntegerField()),
                ("price_per_person", models.DecimalField(decimal_places=2, max_digits=10)),
                ("includes_hotel", models.BooleanField(default=True)),
                ("includes_transport", models.BooleanField(default=True)),
                ("itinerary", models.TextField()),
                ("image_url", models.URLField(blank=True)),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="packages",
                        to="travel.destination",
                    ),
                ),
            ],
            options={"ordering": ["price_per_person", "duration_days"]},
        ),
        migrations.CreateModel(
            name="Hotel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=140)),
                ("address", models.CharField(max_length=220)),
                ("star_rating", models.PositiveSmallIntegerField(default=3)),
                ("price_per_night", models.DecimalField(decimal_places=2, max_digits=10)),
                ("rooms_available", models.PositiveIntegerField(default=10)),
                ("amenities", models.CharField(blank=True, max_length=255)),
                ("image_url", models.URLField(blank=True)),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hotels",
                        to="travel.destination",
                    ),
                ),
            ],
            options={"ordering": ["price_per_night", "name"]},
        ),
        migrations.CreateModel(
            name="TransportOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source", models.CharField(max_length=120)),
                (
                    "transport_type",
                    models.CharField(
                        choices=[("plane", "Plane"), ("train", "Train"), ("bus", "Bus"), ("cab", "Cab")],
                        max_length=20,
                    ),
                ),
                ("provider_name", models.CharField(max_length=120)),
                ("departure_time", models.TimeField()),
                ("arrival_time", models.TimeField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("seats_available", models.PositiveIntegerField(default=30)),
                (
                    "destination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transport_options",
                        to="travel.destination",
                    ),
                ),
            ],
            options={"ordering": ["price", "departure_time"]},
        ),
        migrations.CreateModel(
            name="TripBooking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                (
                    "booking_type",
                    models.CharField(
                        choices=[("hotel", "Hotel"), ("transport", "Transport"), ("package", "Holiday Package")],
                        max_length=20,
                    ),
                ),
                ("check_in_date", models.DateField(blank=True, null=True)),
                ("check_out_date", models.DateField(blank=True, null=True)),
                ("travel_date", models.DateField(blank=True, null=True)),
                ("travelers", models.PositiveSmallIntegerField(default=1)),
                ("special_request", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "destination",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="travel.destination"),
                ),
                (
                    "holiday_package",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="travel.holidaypackage",
                    ),
                ),
                (
                    "hotel",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="travel.hotel",
                    ),
                ),
                (
                    "transport",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="travel.transportoption",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
