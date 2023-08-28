from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("listings", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("newAuction", views.newAuction, name="newAuction"),
    path("viewAuction/<auctionId>", views.viewAuction, name="viewAuction"),
    path("deleteAuction/<auctionId>", views.deleteAuction, name="deleteAuction"),
    path("watchlistAdd/<auctionId>", views.addAuctionToWatchlist, name="watchlistAdd"),
    path("commentAdd/<auctionId>", views.addComment, name="commentAdd"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("wins", views.winsView, name="winsView"),
    path("losses", views.lossesView, name="lossesView")
]
