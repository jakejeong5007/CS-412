from django.shortcuts import render
import random

QUOTES = [
    "Life is like riding a bicycle. To keep your balance, you must keep moving.",
    "Imagination is more important than knowledge.",
    "Try not to become a man of success, but rather try to become a man of value.",
]

IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/d/d3/Albert_Einstein_Head.jpg",
    "https://www.fineartstorehouse.com/p/629/albert-einstein-smoking-pipe-39412547.jpg.webp",
    "https://hips.hearstapps.com/hmg-prod/images/albert-einstein-sticks-out-his-tongue-when-asked-by-news-photo-1681316749.jpg",
]


def quote(request):
    """
    Main page view: pick 1 random quote and 1 random image.
    Template: quote.html
    """
    context = {
        "quote": random.choice(QUOTES),
        "image": random.choice(IMAGES),
    }
    return render(request, "quotes/quote.html", context)


def show_all(request):
    """
    Show all quotes and all images.
    Template: show_all.html
    """
    context = {
        "quotes": QUOTES,
        "images": IMAGES,
    }
    return render(request, "quotes/show_all.html", context)


def about(request):
    """
    About page.
    Template: about.html
    """
    return render(request, "quotes/about.html")
