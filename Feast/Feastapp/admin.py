from django.contrib import admin
from .models import Customer, FoodItem, DeliveryBoy, Order, Address

admin.site.register(Customer)
admin.site.register(FoodItem)
admin.site.register(DeliveryBoy)
admin.site.register(Order)
admin.site.register(Address)
