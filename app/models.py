from django.db import models

class UserDetails(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    pass_word = models.CharField(max_length=200)
    account_type = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class AgentVehicle(models.Model):
    vehicle_registration = models.CharField(max_length=50)
    vin_number = models.CharField(max_length=17)
    vehicle_year = models.PositiveIntegerField()
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    mileage = models.PositiveIntegerField()
    number_etched_into_windows = models.CharField(max_length=50)
    vehicle_name = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    email = models.EmailField()

    agent_id = models.PositiveIntegerField()

    def __str__(self):
        return self.vehicle_registration
