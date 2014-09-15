from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=250)
    display_name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)

class Auctions(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=250)
    description = models.TextField()
    min_bid = models.DecimalField(decimal_places=2, max_digits=10)
    start_price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    current_bid = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    winner = models.ForeignKey(User, null=True, blank=True)

class Bid(models.Model):
    auctions = models.ForeignKey(Auctions)
    created_by = models.ForeignKey(User)
    bid_amount = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    is_auto_bid = models.BooleanField(default=0)
    max_auto_bid = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    auto_bid_queue_num = models.IntegerField(default=0)

    class Meta:
      get_latest_by = 'created_at'

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    favorite_auctions = models.ManyToManyField(Auctions)


