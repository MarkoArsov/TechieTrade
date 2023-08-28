from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment


def home(request):
    return render(request, "auctions/home.html", {
        "auctions": Listing.objects.filter(isOpen=True).order_by("-datetime").all()
    })


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Listing.objects.filter(isOpen=True).order_by("-datetime").all()
    })


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
        return render(request, "auctions/login.html", {
            "big_footer": True
        })


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
        return render(request, "auctions/register.html", {
            "big_footer": True
        })


def profile(request):
    if not request.user.is_authenticated:
        return login_view(request)
    return render(request, "auctions/profile.html", {
        "auctions": request.user.listings.order_by("-datetime").all()
    })


def addAuctionToWatchlist(request, auctionId):
    if not request.user.is_authenticated:
        return login_view(request)
    listing = Listing.objects.get(pk=auctionId)
    request.user.watchlist.add(listing)
    return viewAuction(request, auctionId)


def newAuction(request):
    if not request.user.is_authenticated:
        return login_view(request)
    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["desc"]
        startBid = request.POST["start"]
        img = request.POST["img"]
        currentUserId = request.user.id
        newListing = Listing(title=title, description=desc, currentBidValue=startBid, user_id=currentUserId,
                             isOpen=True, winner_id=currentUserId, image=img)
        newListing.save()
        return index(request)
    return render(request, "auctions/newAuction.html", {
        "big_footer": True
    })


def viewAuction(request, auctionId):
    listing = Listing.objects.get(pk=auctionId)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return index(request)
        newBidValue = request.POST["newBid"]
        if float(newBidValue) > float(listing.currentBidValue):
            listing.currentBidValue = newBidValue
            listing.losers.add(listing.winner)

            if request.user in listing.losers.all():
                listing.losers.remove(request.user)

            listing.winner_id = request.user.id
            request.user.watchlist.add(listing)
            listing.save()

            newBid = Bid(user_id=request.user.id, listing_id=listing.id, value=float(newBidValue))
            newBid.save()
    return render(request, "auctions/viewAuction.html", {
        "auction": listing,
        "comments": listing.comments.order_by("-datetime").all(),
        "winner": listing.winner.username,
        "losers": listing.losers.all()
    })


def deleteAuction(request, auctionId):
    listing = Listing.objects.get(pk=auctionId)
    listing.isOpen = False
    listing.save()
    return profile(request)


def addComment(request, auctionId):
    if not request.user.is_authenticated:
        return index(request)
    if request.method == "POST":
        listing = Listing.objects.get(pk=auctionId)
        commentContent = request.POST["content"]
        newComment = Comment(user_id=request.user.id, listing_id=listing.id, content=commentContent)
        newComment.save()
        request.method = "GET"
    return viewAuction(request, auctionId)


def watchlist(request):
    if not request.user.is_authenticated:
        return login_view(request)
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.order_by("-datetime").all()
    })


def winsView(request):
    return render(request, "auctions/wins.html", {
        "wins": request.user.wins.filter(isOpen=False).order_by("-datetime").all()
    })


def lossesView(request):
    return render(request, "auctions/losses.html", {
        "losses": request.user.losses.filter(isOpen=False).order_by("-datetime").all()
    })
