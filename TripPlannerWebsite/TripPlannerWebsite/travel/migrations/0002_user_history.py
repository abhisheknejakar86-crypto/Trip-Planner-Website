# Generated for per-user bookings and browsing history.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("travel", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="tripbooking",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="trip_bookings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="BrowsingHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "item_type",
                    models.CharField(
                        choices=[
                            ("destination", "Destination"),
                            ("hotel", "Hotel"),
                            ("transport", "Transport"),
                            ("package", "Holiday Package"),
                        ],
                        max_length=20,
                    ),
                ),
                ("item_name", models.CharField(max_length=160)),
                ("destination_name", models.CharField(blank=True, max_length=120)),
                ("price", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("image_url", models.URLField(blank=True)),
                ("notes", models.CharField(blank=True, max_length=255)),
                ("viewed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="browsing_history",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "browsing history",
                "ordering": ["-viewed_at"],
            },
        ),
    ]
