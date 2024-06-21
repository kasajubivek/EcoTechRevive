from django.db import models

class Device(models.Model):
    DEVICE_TYPES = [
        ('Smartphone', 'Smartphone'),
        ('Tablet', 'Tablet'),
        ('Laptop', 'Laptop'),
    ]

    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, unique=True)
    date_received = models.DateField()
    is_functional = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.serial_number})"


class Refurbishment(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    date_started = models.DateField()
    date_completed = models.DateField(null=True, blank=True)
    description = models.TextField()
    technician = models.CharField(max_length=100)

    def __str__(self):
        return f"Refurbishment for {self.device}"


class QualityAssurance(models.Model):
    refurbishment = models.ForeignKey(Refurbishment, on_delete=models.CASCADE)
    date_checked = models.DateField()
    checked_by = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    notes = models.TextField()

    def __str__(self):
        return f"QA for {self.refurbishment.device}"


class CustomerSupport(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    response = models.TextField(null=True, blank=True)
    date_responded = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Support request from {self.name} ({self.email})"
from django.db import models

# Create your models here.
