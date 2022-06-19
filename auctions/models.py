from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    datetime = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    currentBidValue = models.DecimalField(max_digits=10, decimal_places=2)
    imageURL = models.CharField(max_length=256)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    watchListUsers = models.ManyToManyField(User, related_name="watchlist")

    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wins")
    losers = models.ManyToManyField(User, related_name="losses")

    isOpen = models.BooleanField()

    def setCurrentBid(self, bidValue):
        self.currentBidValue = bidValue

    def getCurrentBid(self):
        return self.bids.get(value=self.currentBidValue)


class Bid(models.Model):
    datetime = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    value = models.DecimalField(max_digits=10, decimal_places=2)


class Comment(models.Model):
    datetime = models.DateTimeField(auto_now=True)

    content = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="allComments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
