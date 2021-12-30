from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing_page/<int:auction_id>", views.listing_page, name="listing_page"),
    path("bid/<int:auction_id>", views.bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:auction_id>", views.add_watchlist, name="add_watchlist"),
    path("watchlist/remove/<int:auction_id>", views.remove_watchlist, name="remove_watchlist"),
    path("comment/<int:auction_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("active_listing/<str:category>", views.active_listing, name="active_listing"),
    path("my_listings/<str:lister>", views.my_listings, name="my_listings"),
    path("close/<int:auction_id>", views.close, name="close"),
    path("profile", views.profile, name="profile"),
    path("edit_me", views.edit_me, name="edit_me"),
    path("unbid/<int:auction_id>", views.unbid, name="unbid")
]
