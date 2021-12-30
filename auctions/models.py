from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    highest_bid = models.IntegerField(null=True)
    image = models.URLField(blank=True)
    catg = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.IntegerField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bid by: {self.name}, Amount: {self.bid}, Listing: {self.auction} time: {self.timestamp}"

class Comment(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Name: {self.name}, comment: {self.comment}, Commented on: {self.auction}"

class WatchList(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    auctions = models.ManyToManyField(Auction, related_name='lists')

    def __str__(self):
        return f"{self.auctions}"

class Lister(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.auction}"

class Winner(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    win = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} won - {self.win}"

class Category(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"
