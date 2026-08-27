from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/<str:service>/", views.service_search, name="service_search"),
    path("hotels/", views.hotels, name="hotels"),
    path("hotels/<int:pk>/", views.hotel_detail, name="hotel_detail"),
    path("transport/", views.transport, name="transport"),
    path("transport/<int:pk>/", views.transport_detail, name="transport_detail"),
    path("packages/", views.packages, name="packages"),
    path("packages/<int:pk>/", views.package_detail, name="package_detail"),
    path("destinations/<int:pk>/", views.destination_detail, name="destination_detail"),
    path("book/", views.book_trip, name="book_trip"),
    path("booking-success/", views.booking_success, name="booking_success"),
]
