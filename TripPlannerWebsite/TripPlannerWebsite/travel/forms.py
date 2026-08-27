from django import forms

from .models import TripBooking


class TripSearchForm(forms.Form):
    destination = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search destination, hotel, or package"}),
    )
    travel_type = forms.ChoiceField(
        required=False,
        choices=[
            ("", "All travel methods"),
            ("plane", "Plane"),
            ("train", "Train"),
            ("bus", "Bus"),
            ("cab", "Cab"),
        ],
    )
    max_budget = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"placeholder": "Max budget"}),
    )


class TripBookingForm(forms.ModelForm):
    class Meta:
        model = TripBooking
        fields = [
            "customer_name",
            "email",
            "phone",
            "booking_type",
            "destination",
            "hotel",
            "transport",
            "holiday_package",
            "check_in_date",
            "check_out_date",
            "travel_date",
            "travelers",
            "special_request",
        ]
        widgets = {
            "check_in_date": forms.DateInput(attrs={"type": "date"}),
            "check_out_date": forms.DateInput(attrs={"type": "date"}),
            "travel_date": forms.DateInput(attrs={"type": "date"}),
            "special_request": forms.Textarea(attrs={"rows": 4}),
        }
