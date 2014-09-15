from django.core.management.base import BaseCommand, CommandError
from auction.models import Auctions, Bid
from django.contrib.auth.models import User
import datetime
from django.core.mail import send_mail
from datetime import timedelta, date
from django.utils import timezone

class Command(BaseCommand):

    def handle(self, *args, **options):
        today_min = datetime.datetime.combine(timezone.now(), datetime.time.min)
        today_max = datetime.datetime.combine(timezone.now()+ timedelta(days=1), datetime.time.max)

        auctions = Auctions.objects.filter(end_date__range=(today_min, today_max))

        for auction in auctions:
            won_bid = Bid.objects.latest()
            if(won_bid != None):
                auction.winner = won_bid.created_by
                auction.save()
                send_mail('Auction TEST', 'You have won the auction!', 'alexdolgov88@gmail.com',
                    [won_bid.created_by.email], fail_silently=False)
