from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    def get_price_in_cents(self):
        """Stripe работает в центах/копейках"""
        return int(self.price * 100)