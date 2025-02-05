from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class DeliveryBoy(models.Model):
    STATUS_CHOICES = [
        ('not_accepted', 'Not Accepted'),
        ('accepted', 'Accepted'),
    ]
    full_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_accepted')

    def __str__(self):
        return self.full_name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    door_no = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.door_no}, {self.street}, {self.area}, {self.pincode}"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Delivered', 'Delivered'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.SET_NULL, null=True, blank=True)
    accepted_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.customer.name}"