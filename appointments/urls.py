from django.urls import path
from .views import book_appointment, user_appointments

urlpatterns = [
    path("book/appointment/", book_appointment, name="book-appointment"),
     path('get/appointments/', user_appointments, name='user-appointments'),
]