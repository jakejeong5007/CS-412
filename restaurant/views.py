from django.shortcuts import render
import random
import time

# Daily specials 
DAILY_SPECIALS = [
    {"name": "Kimchi Fried Rice", "price": 9.99},
    {"name": "Bulgogi Bowl", "price": 12.49},
    {"name": "Spicy Ramen", "price": 11.25},
]

# Menu items
MENU = {
    "item1": {"label": "Tteokbokki", "price": 7.50},
    "item2": {"label": "Kimbap", "price": 5.25},
    "item3": {"label": "Fried Dumplings", "price": 6.75},
    "item4": {"label": "Bubble Tea", "price": 4.99},
}


def main(request):
    """
    Main page view.
    Just render main.html.
    """
    return render(request, "restaurant/main.html")


def order(request):
    """
    Ordering page view.
    Choose a daily special randomly and pass it to order.html.
    """
    special = random.choice(DAILY_SPECIALS)
    context = {
        "daily_special": special, 
        "menu": MENU,             
    }
    return render(request, "restaurant/order.html", context)


def confirmation(request):
    """
    Process the submitted order form and display confirmation page.
    - Determine which items were ordered from POST data
    - Compute total price
    - Pass ordered items + total to confirmation.html
    """
    if request.method != "POST":
        return render(request, "restaurant/confirmation.html", {
            "ordered_items": [],
            "total": 0.0,
            "error": "Please submit an order from the order page.",
        })

    ordered_items = []
    total = 0.0

    for key, meta in MENU.items():
        if request.POST.get(key):
            ordered_items.append(meta["label"])
            total += meta["price"]

    if request.POST.get("daily_special"):
        special_name = request.POST.get("daily_special_name")
        special_price = request.POST.get("daily_special_price")

        if special_name and special_price:
            try:
                price_val = float(special_price)
            except ValueError:
                price_val = 0.0
            ordered_items.append(special_name)
            total += price_val
        else:
            # Fallback if hidden inputs weren't included
            special = random.choice(DAILY_SPECIALS)
            ordered_items.append(special["name"])
            total += special["price"]

    # Customer info fields
    customer_name = request.POST.get("name", "").strip()
    phone = request.POST.get("phone", "").strip()
    email = request.POST.get("email", "").strip()
    instructions = request.POST.get("instructions", "").strip()

    now = time.time() 
    estimated_time = now + random.randint(30*60, 60*60) 
    estimated_time = time.strftime("%H:%M", time.localtime(estimated_time))
    curr_time = time.strftime("%H:%M", time.localtime(time.time()))
    
    context = {
        "ordered_items": ordered_items,
        "total": round(total, 2),
        "customer_name": customer_name,
        "phone": phone,
        "email": email,
        "instructions": instructions,
        "estimated_time": estimated_time,
        "curr_time": curr_time,
    }
    return render(request, "restaurant/confirmation.html", context)
