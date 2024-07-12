from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Uploaded file by {self.user.username} at {self.uploaded_at}"


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_date = models.DateField()
    visit_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Session for {self.user.username} on {self.session_date}"


class UserProfile(models.Model):
    SECURITY_QUESTIONS = [
        ('What was your childhood nickname?', 'What was your childhood nickname?'),
        ('What is the name of your favorite childhood friend?', 'What is the name of your favorite childhood friend?'),
        ('What was your dream job as a child?', 'What was your dream job as a child?'),
        ('What is the name of your first pet?', 'What is the name of your first pet?'),
        ('What was the model of your first car?', 'What was the model of your first car?'),
        ('What elementary school did you attend?', 'What elementary school did you attend?')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    security_question_1 = models.CharField(max_length=255, choices=SECURITY_QUESTIONS)
    security_answer_1 = models.CharField(max_length=255)
    security_question_2 = models.CharField(max_length=255, choices=SECURITY_QUESTIONS)
    security_answer_2 = models.CharField(max_length=255)
    security_question_3 = models.CharField(max_length=255, choices=SECURITY_QUESTIONS)
    security_answer_3 = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    name = models.CharField(max_length=40)
    product_image = models.ImageField(upload_to='product_image/', null=True, blank=True)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=40)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart}"



@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_cart(sender, instance, **kwargs):
    instance.cart.save()



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.id}"


