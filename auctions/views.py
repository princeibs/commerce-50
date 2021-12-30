from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime as dt

from .models import *


def index(request):
    context = {
        # Return the active listings
        "active_auctions": Auction.objects.filter(is_active=True).all(),
        "closed_auctions": Auction.objects.filter(is_active=False).all()
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        # Get the details submitted from the form
        title = request.POST["title"]
        desc = request.POST["description"]
        s_bid = request.POST["starting_bid"]
        img = request.POST["img_url"]
        catg = request.POST["category"]

        # Save details into respective model in the database.
        auction = Auction.objects.create(title=title, description=desc, starting_bid=s_bid, image=img, catg=catg)
        auction.save()
        lister = Lister.objects.create(name=request.user, auction=auction)
        lister.save
        category = Category.objects.create(auction=auction, category=catg)
        category.save()

        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, 'auctions/create_listing.html')

def listing_page(request, auction_id):

    # Handles Anonymous users.
    user = request.user
    if request.user == AnonymousUser():
        user = None

    auction = Auction.objects.get(pk=auction_id)
    bidded = False
    in_watchlist = False
    close = False
    is_me = False
    winner = None
    has_bid = False
    min_bid = 0

    # Checks who won an inactive auction
    if not auction.is_active:
        # If the logged in user won
        try:
            winner = Winner.objects.get(win=auction).name
            if user == winner:
                is_me = True
        # Set the value of winner to None
        except Winner.DoesNotExist:
            pass

    # Checks if the user has already placed a bid
    try:
        Bid.objects.get(name=user, auction=auction)
        bidded = True
    except Bid.DoesNotExist:
        bidded = False

    # Checks if user already added auction to watchlist
    try:
        WatchList.objects.get(name=user, auctions=auction)
        in_watchlist = True
    except WatchList.DoesNotExist:
        in_watchlist = False

    except Bid.DoesNotExist:
        pass
    # Checks if the logged in user placed the Auction
    if user == Lister.objects.get(auction=auction).name:
        close = True

    bids = Bid.objects.filter(auction=auction).count()
    if bids > 0:
        has_bid = True
        min_bid = auction.highest_bid + 1

    context = {
        "comments": Comment.objects.filter(auction=auction_id).all(),
        "lister": Lister.objects.get(auction=auction),
        "bidded": bidded,
        "close": close,
        "bids": bids,
        "auction": auction,
        "in_watchlist": in_watchlist,
        "is_active": auction.is_active,
        "is_me": is_me,
        "winner": winner,
        "has_bid": has_bid,
        "min_bid": min_bid,
    }
    return render(request, 'auctions/listing_page.html', context)

@login_required(login_url='login')
def bid(request, auction_id):

    if request.method == "POST":
        name = request.user
        bid = request.POST["bid_amount"]
        auction = Auction.objects.get(pk=auction_id)
        bids = Bid.objects.filter(auction=auction).all()

        new_bid = Bid.objects.create(name=name, bid=bid, auction=auction)
        new_bid.save()
        bids = Bid.objects.filter(auction=auction).all()
        uni = []
        for i in bids:
            uni.append(i.bid)
        auction.highest_bid = max(uni)
        auction.save()

        return HttpResponseRedirect(reverse("listing_page", args=(auction_id,)))
    else:
        return HttpResponseRedirect(reverse("listing_page", args=(auction_id,)))

def unbid(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    Bid.objects.get(name=request.user, auction=auction).delete()

    bids = Bid.objects.filter(auction=auction).all()
    auction.highest_bid = 0
    if len(bids) > 0:
        uni = []
        for i in bids:
            uni.append(i.bid)
        auction.highest_bid = max(uni)

    auction.save()
    return HttpResponseRedirect(reverse("listing_page", args=(auction_id,)))

@login_required(login_url='login')
def watchlist(request):
    try:
        # Get all of the logged in user's watchlist
        watchlists = WatchList.objects.get(name=request.user).auctions.all()
    except WatchList.DoesNotExist:
        return render(request, "auctions/watchlist.html", {"message": "No watchlist added yet"})

    context = {
        "watchlists": watchlists,
    }
    return render(request, "auctions/watchlist.html", context)

@login_required(login_url='login')
def add_watchlist(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    # Try to add listing to users watchlist
    try:
        WatchList.objects.get(name=request.user).auctions.add(auction)
    except WatchList.DoesNotExist:
        # Creates a watchlist object of None is found
        my_watchlist = WatchList.objects.create(name=request.user)
        my_watchlist.auctions.add(auction)
        my_watchlist.save()

    return HttpResponseRedirect(reverse('watchlist'))

@login_required(login_url='login')
def remove_watchlist(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    WatchList.objects.get(name=request.user).auctions.remove(auction)
    return HttpResponseRedirect(reverse('watchlist'))

@login_required(login_url='login')
def comment(request, auction_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        name = request.user
        auction = Auction.objects.get(pk=auction_id)

        my_comment = Comment.objects.create(name=name, comment=comment, auction=auction)
        my_comment.save()
        return HttpResponseRedirect(reverse("listing_page", args=(auction_id,)))

    else:
        return HttpResponseRedirect(reverse("listing_page", args=(auction_id,)))

def categories(request):
    categories = Category.objects.distinct()
    context = {
        "categories": list(set(categories))
    }
    return render(request, "auctions/categories.html", context)

def active_listing(request, category):
    listings = Auction.objects.filter(catg=category)
    active_listings = listings.filter(is_active=True)
    non_active_listings = listings.filter(is_active=False)
    context = {
        "active_listings": active_listings,
        "non_active_listings": non_active_listings
    }
    return render(request, "auctions/active_listing.html", context)

def my_listings(request, lister):
    lister = User.objects.get(username=lister)
    lists = Lister.objects.filter(name=lister).all()
    context = {
        "lists": lists,
        "lister": lister,
    }
    return render(request, "auctions/my_listings.html", context)

def close(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    # Deactivates the auction
    auction.is_active=False
    auction.save()
    # Get the starting bid
    try:
        largest_bid = auction.highest_bid
        # Get the largest bidder and make them the winner
        bidder = Bid.objects.get(bid=largest_bid, auction=auction).name
        winner = Winner.objects.create(name=bidder, win=auction)
        winner.save()
    except Bid.DoesNotExist:
        pass

    return HttpResponseRedirect(reverse("listing_page", args=(auction_id,)))

@login_required(login_url='login')
def profile(request):
    user = request.user

    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'last_login': user.last_login,
        'date_joined': user.date_joined,
    }
    return render(request, "auctions/profile.html", context)

@login_required(login_url='login')
def edit_me(request):
    user = request.user

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        new_password = request.POST["new_password"]
        confirm_new_password = request.POST["confirm_new_password"]

        # Validates the passwords entered
        if not (user.check_password(password) and (new_password == confirm_new_password)):
            return render(request, "auctions/edit_me.html", {"message": "Enter valid passwords"})
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.set_password(new_password)
            user.save()

            return HttpResponseRedirect(reverse("profile"))
    else:
        context = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'message': None
        }
        return render(request, "auctions/edit_me.html", context)
