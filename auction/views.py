from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from auction.models import Category, Auctions, Bid, UserProfile
import operator
from decimal import Decimal
from django.db.models import Max
from datetime import datetime, timedelta
from django.utils import timezone
from django.template import RequestContext

def index(request):
    category_list = Category.objects.order_by('display_name')
    context = {'category_list':category_list}
    return render(request, 'auction.html', context)

def auctions_list(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    auctions = Auctions.objects.filter(category_id=category.id)
    return render(request, 'auctions_list.html', {'auctions' : auctions, 'category' : category})

def details(request, category_name, auction_id):

    fmt = '%Y-%m-%d %H:%M:%S %Z'

    auction = get_object_or_404(Auctions, pk=auction_id)
    bids = Bid.objects.filter(auctions=auction_id)

    if(auction.current_bid > 0):
        current_bid = auction.current_bid
    else:
        current_bid = auction.start_price

    start = auction.start_date + timedelta(hours=-4)
    end = auction.end_date + timedelta(hours=-4)

    is_start = start < timezone.now()
    is_end = end < timezone.now()

    favorites = UserProfile.objects.filter(favorite_auctions__id=auction.id)

    if(favorites.count() > 0):
        in_favorites = True
    else:
        in_favorites = False

    return render(request, 'details.html', {'auction' : auction, 'current_bid' : current_bid, 'bids' : bids,
                                            'is_start' : is_start, 'is_end' : is_end, 'start_date' : start,
                                            'in_favorites' : in_favorites
                                            })

def bid(request):

    if request.method == 'POST':

        auction = Auctions.objects.filter(id=request.POST['auction_id'])[:1].get()

        bid_amount = request.POST['bid_amount']
        created_by = request.user
        max_auto_bid = 0

        is_auto_bid = request.POST.get('is_auto_bid', False)

        if(is_auto_bid == False):

            auto_bids = Bid.objects.filter(is_auto_bid=True, auctions_id=auction.id, max_auto_bid__gte=bid_amount)
            if(auto_bids.count() > 0):

                earlest_auto_bids = sorted(auto_bids, key=operator.attrgetter('created_at'))

                earlest_auto_bid = earlest_auto_bids[0]

                bid_amount = bid_amount
                is_auto_bid = True
                created_by = earlest_auto_bid.created_by
                max_auto_bid = earlest_auto_bid.max_auto_bid

            auction.current_bid = bid_amount

        else:

            auto_bids = Bid.objects.filter(is_auto_bid=True, auctions_id=auction.id,
                                           max_auto_bid__gte=request.POST['max_auto_bid']).exclude(created_by=request.user)

            if(auto_bids.count() > 0):

                earlest_auto_bids = sorted(auto_bids, key=operator.attrgetter('created_at'))

                earlest_auto_bid = earlest_auto_bids[0]

                if(earlest_auto_bid.max_auto_bid == Decimal(request.POST['max_auto_bid'])):

                    bid_amount = earlest_auto_bid.max_auto_bid

                else:

                    bid_amount = Decimal(request.POST['max_auto_bid']) + auction.min_bid

                is_auto_bid = True
                created_by = earlest_auto_bid.created_by
                max_auto_bid = earlest_auto_bid.max_auto_bid
            else:
                max_bid = Bid.objects.filter(is_auto_bid=True, auctions_id=auction.id).aggregate(Max('max_auto_bid'))
                is_auto_bid = True
                max_auto_bid = request.POST['max_auto_bid']

                if(max_bid['max_auto_bid__max'] == 0 or max_bid['max_auto_bid__max'] == None):
                    bid_amount = auction.current_bid + auction.min_bid
                else:
                    bid_amount = max_bid['max_auto_bid__max'] + auction.min_bid


            auction.current_bid = bid_amount

        new_bid = Bid(auctions = auction,
                      bid_amount = bid_amount,
                      is_auto_bid = is_auto_bid,
                      created_by = created_by,
                      max_auto_bid = max_auto_bid)

        auction.save()
        new_bid.save()

        return HttpResponseRedirect('/home')

    else:
        return render(request, 'home.html', {})

def profile(request):

    auctions_in_run = []
    won_auctions = []

    auction_ids = request.user.bid_set.values_list('auctions').distinct()

    if(auction_ids.count() > 0):
        auctions_in_run = Auctions.objects.filter(id__in=auction_ids, winner=None)
        won_auctions = Auctions.objects.filter(id__in=auction_ids, winner=request.user)

    favorite = request.user.userprofile.favorite_auctions.all()

    return render(request, 'profile.html', {'user' : request.user,
                                            'auctions_in_run' : auctions_in_run,
                                            'won_auctions' : won_auctions,
                                            'favorite_auctions' : favorite})

def favorites(request):
    context = RequestContext(request)
    auction_id = None
    to_add = None

    if request.method == 'POST':
        auction_id = request.POST['auction_id']

    if auction_id:
        userProfile = UserProfile.objects.get(user=request.user)
        auction = Auctions.objects.get(id=auction_id)

        if(auction.userprofile_set.filter(id=userProfile.id).exists()):
            userProfile.favorite_auctions.remove(auction)
        else:
            userProfile.favorite_auctions.add(auction)


        userProfile.save()

    return HttpResponse()