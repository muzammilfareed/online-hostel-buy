from django.db import models
from authen_app.models import CustomUser
# Create your models here.


class house_info(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.TextField(default='')
    address = models.TextField(default='')
    phone_number = models.TextField(default='')
    # longitude = models.TextField(default='')
    # latitude = models.TextField(default='')
    location = models.TextField(default='')
    description = models.TextField(default='')
    additional_info = models.TextField(default='')
    booker_name = models.TextField(default='')
    booked_by_user_id = models.IntegerField(default=0)
    no_of_rooms = models.IntegerField(default=0)
    square_fit = models.TextField(default=0)
    no_of_bath = models.IntegerField(default=0)
    no_of_kitchen = models.IntegerField(default=0)
    is_electricity = models.BooleanField(default=False)
    is_water = models.BooleanField(default=False)
    is_gas = models.BooleanField(default=False)
    is_internet = models.BooleanField(default=False)
    is_furnished = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_datetime = models.DateTimeField(auto_now=True, blank=True, null=True)
    booking_date = models.DateTimeField(blank=True, null=True)
    rent = models.DecimalField(decimal_places=2, max_digits=10)


class house_images(models.Model):
    house = models.ForeignKey(house_info, on_delete=models.CASCADE)
    image_path = models.TextField(default='')
    created_datetime = models.DateTimeField(auto_now_add=True)


class house_video(models.Model):
    house = models.ForeignKey(house_info, on_delete=models.CASCADE)
    video_path = models.TextField(default='')
    created_datetime = models.DateTimeField(auto_now_add=True)