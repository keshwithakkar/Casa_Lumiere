from django.shortcuts import render, redirect, get_object_or_404
from .models import amenities, about, contact, faq, gallery, terms, Testimonial
from custom_admin.models import Amenity, Testimonial, FAQ, Gallery, ContactUs, ContactEnquiry, Restaurant, Room, Guest, Booking, Coupon, RegisteredUser, MenuItem
from decimal import Decimal
from datetime import datetime, date, timedelta
from django.db.models import Q
from django.db.models import Sum

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password



def home(request):

    rooms = Room.objects.all()[:3]
    amenities = Amenity.objects.all()[:4]
    gallery = Gallery.objects.all()[:10]
    testimonials = Testimonial.objects.all()[:4]

    notification_count = 0

    if request.session.get("user_id"):
        user_id = request.session["user_id"]
        bookings = Booking.objects.filter(user_id=user_id)

        today = date.today()

        for booking in bookings:
            if (
                booking.check_in == today or
                (today < booking.check_in <= today + timedelta(days=2)) or
                booking.booking_status == "Confirmed" or
                booking.booking_status == "Cancelled" or
                booking.check_out < today
            ):
                notification_count += 1

    return render(request, 'home.html', {
        'rooms': rooms,
        'amenities': amenities,
        'gallery': gallery,
        'testimonials': testimonials,
        'notification_count': notification_count   # 👈 ADD THIS
    })

def about_us(request):
    return render(request, 'restaurant/about.html')

def amenities(request):
    indoor_amenities = Amenity.objects.filter(category="Indoor")
    outdoor_amenities = Amenity.objects.filter(category="Outdoor")

    return render(request, "restaurant/amenities.html", {
        "indoor_amenities": indoor_amenities,
        "outdoor_amenities": outdoor_amenities,
    })

def gallery(request):
    gallery_items = Gallery.objects.all()

    context = {
        "gallery_items": gallery_items
    }
    return render(request, "restaurant/gallery.html", context)

def faq(request):
    faqs = FAQ.objects.all().order_by('faq_id')
    return render(request, 'restaurant/faq.html', {'faqs': faqs})

def contact(request):
    contact = ContactUs.objects.first()

    if request.method == "POST":
        ContactEnquiry.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone")
        )
        return redirect('/contact/?success=1#reach-us')

    return render(request, 'restaurant/contact.html', {
        'contact': contact
    })

def terms(request):
    return render(request, 'restaurant/terms.html')

def testimonial(request):
    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")
        image = request.FILES.get("image")

        Testimonial.objects.create(
            name=name,
            message=message,
            image=image
        )

        return redirect("testimonial")

    all_testimonial = Testimonial.objects.all()
    return render(request, "restaurant/testimonial.html", {
        "testimonial": all_testimonial
    })

def restaurant_page(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant/restaurant.html', {
        'restaurants': restaurants
    })

def rooms(request):
    rooms = Room.objects.all().order_by('id')

    checkin = request.GET.get("checkin")
    checkout = request.GET.get("checkout")
    adults = request.GET.get("adults")
    children = request.GET.get("children")
    rooms_requested = int(request.GET.get("rooms", 1))
    currency = request.GET.get("currency", "INR")

    if checkin and checkout:
        checkin_date = datetime.strptime(checkin.strip(), "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout.strip(), "%Y-%m-%d").date()

        for room in rooms:

            # --------- PRICE CALCULATION ---------
            total_price = 0
            current_day = checkin_date

            while current_day < checkout_date:
                price = room.price

                # Saturday = 5, Sunday = 6
                if current_day.weekday() in [5, 6]:
                    price += 1000

                total_price += price
                current_day += timedelta(days=1)

            room.calculated_price = total_price

            # --------- AVAILABILITY ---------
            overlapping = Booking.objects.filter(
                room=room,
                booking_status="Confirmed"
            ).filter(
                Q(check_in__lt=checkout_date) & Q(check_out__gt=checkin_date)
            )

            booked = overlapping.aggregate(
                total=Sum("rooms_booked")
            )["total"] or 0

            room.available_rooms = room.total_rooms - booked

    else:
        for room in rooms:
            room.available_rooms = room.total_rooms
            room.calculated_price = room.price

    return render(request, 'restaurant/rooms.html', {
        'rooms': rooms,
        'checkin': checkin,
        'checkout': checkout,
        'adults': adults,
        'children': children,
        'rooms_requested': rooms_requested,
        "currency": currency
})

def book(request):

    if not request.session.get("user_id"):
        return redirect("login")

    if request.method == "POST":

        # ---------- Guest Data ----------
        name = request.POST.get("name").strip()
        email = request.POST.get("email").strip()
        phone = request.POST.get("phone").strip()

        # ---------- Booking Data ----------
        room_type = request.POST.get("room").strip()
        checkin = request.POST.get("checkin", "").strip()
        checkout = request.POST.get("checkout", "").strip()
        adults = int(request.POST.get("adults"))
        children = int(request.POST.get("children"))
        rooms_booked = int(request.POST.get("rooms"))  # 👈 NEW
        coupon_code = (request.POST.get("coupon") or "").strip()

        # Convert string to date
        checkin = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout = datetime.strptime(checkout, "%Y-%m-%d").date()

        # Get Room object
        room = Room.objects.filter(room_type=room_type).first()
        if not room:
            return redirect("rooms")

        # 🚨 Check availability
        # 🚨 Check availability properly by date overlap
        overlapping_bookings = Booking.objects.filter(
            room=room,
            booking_status="Confirmed"
        ).filter(
            Q(check_in__lt=checkout) & Q(check_out__gt=checkin)
        )

        rooms_already_booked = overlapping_bookings.aggregate(
            total=Sum("rooms_booked")
        )["total"] or 0

        available_rooms = room.total_rooms - rooms_already_booked

        if available_rooms < rooms_booked:
            return render(request, "restaurant/book.html", {
                "error": "Not enough rooms available for selected dates!"
            })

        # Create or Get Guest
        guest, created = Guest.objects.get_or_create(
            email=email,
            defaults={
                "name": name,
                "phone": phone
            }
        )

        # ---------- Price Calculation ----------
        currency = request.POST.get("currency", "INR")

        room_price = Decimal(request.POST.get("room_price"))
        extra_guest_price = Decimal(request.POST.get("extra_guest_price"))
        tax_price = Decimal(request.POST.get("tax_price"))
        discount_price = Decimal(request.POST.get("discount_price"))
        total_price = Decimal(request.POST.get("total_price"))

        # Convert EUR → INR before saving
        exchange_rate = Decimal("90")

        if currency == "EUR":
            room_price = room_price * exchange_rate
            extra_guest_price = extra_guest_price * exchange_rate
            tax_price = tax_price * exchange_rate
            discount_price = discount_price * exchange_rate
            total_price = total_price * exchange_rate

        user_id = request.session.get("user_id")
        registered_user = RegisteredUser.objects.get(id=user_id)
       
        # ---------- Save Booking ----------
        booking = Booking.objects.create(
            user=registered_user,
            guest=guest,
            room=room,
            check_in=checkin,
            check_out=checkout,
            adults=adults,
            children=children,
            rooms_booked=rooms_booked,
            room_price=room_price,
            extra_guest_price=extra_guest_price,
            tax_price=tax_price,
            discount_price=discount_price,
            total_price=total_price,
            coupon_code=coupon_code if coupon_code else None,
            booking_status="Confirmed"
        )

        action_type = request.POST.get("action_type")

        if action_type == "invoice":
            return redirect("invoice", booking_id=booking.id)

        return redirect("home")

    # -------- GET METHOD --------
    context = {
        "checkin": request.GET.get("checkin"),
        "checkout": request.GET.get("checkout"),
        "adults": request.GET.get("adults"),
        "children": request.GET.get("children"),
        "room": request.GET.get("room"),
        "price": request.GET.get("price"),
        "rooms": request.GET.get("rooms"),  # 👈 ADD THIS
        "currency": request.GET.get("currency", "INR"),
    }

    return render(request, "restaurant/book.html", context)


def my_bookings(request):

    if not request.session.get("user_id"):
        return redirect("login")

    user_id = request.session["user_id"]

    bookings = Booking.objects.filter(user_id=user_id).order_by("-check_in")

    return render(request,"restaurant/my_bookings.html",{
        "bookings": bookings,
        "today": date.today()   # 👈 ADD THIS
})

def cancel_booking(request, booking_id):

    if not request.session.get("user_id"):
        return redirect("login")

    user_id = request.session["user_id"]

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user_id=user_id
    )

    if request.method == "POST":
        booking.booking_status = "Cancelled"
        booking.save()

    return redirect("my_bookings")

def signup(request):
    if request.method == "POST":

        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        # username already exists
        if RegisteredUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        if RegisteredUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("signup")

        # Save in RegisteredUser table
        RegisteredUser.objects.create(
            username=username,
            email=email,
            password=make_password(password)   # encrypted password
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "restaurant/signup.html")

def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()

        try:
            user = RegisteredUser.objects.get(username=username)

            # check encrypted password
            if check_password(password, user.password):

                # create session
                request.session["user_id"] = user.id
                request.session["username"] = user.username

                return redirect("home")

            else:
                messages.error(request, "Incorrect password.")

        except RegisteredUser.DoesNotExist:
            messages.error(request, "Username not found.")

    return render(request, "restaurant/login.html")


def logout_view(request):
    request.session.flush()
    return redirect("home")


def manage_profile(request):

    # check login
    if not request.session.get("user_id"):
        return redirect("login")

    user_id = request.session["user_id"]
    user = RegisteredUser.objects.get(id=user_id)

    if request.method == "POST":

        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # update username and email
        user.username = username
        user.email = email

        # update password if entered
        if password:
            if password == confirm_password:
                user.password = make_password(password)
            else:
                messages.error(request, "Passwords do not match.")
                return redirect("manage_profile")

        user.save()

        # update session username
        request.session["username"] = user.username

        messages.success(request, "Profile updated successfully!")

        return redirect("manage_profile")

    return render(request, "restaurant/manage_profile.html", {
        "user": user
    })


def menu(request):
    menu_items = MenuItem.objects.select_related('restaurant').all()

    return render(request, "restaurant/menu.html", {
        "menu_items": menu_items
    })


def invoice_page(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)

    return render(request, "restaurant/invoice.html", {
        "booking": booking
    })


def notifications(request):

    if not request.session.get("user_id"):
        return redirect("login")

    user_id = request.session["user_id"]
    bookings = Booking.objects.filter(user_id=user_id)

    today = date.today()
    notification_list = []

    for booking in bookings:

        # 🟢 Stay Starts Today
        if booking.check_in == today:
            notification_list.append({
                "type": "success",
                "message": f" Your getaway begins today. Your {booking.room.room_type} is ready to welcome you — step in and unwind in comfort."
            })

        # 🟡 Upcoming Booking
        if today < booking.check_in <= today + timedelta(days=2):
            notification_list.append({
                "type": "warning",
                "message": f" Your stay is just around the corner on {booking.check_in}. A beautiful experience awaits you."
            })

        # 🔵 Booking Confirmed
        if booking.booking_status == "Confirmed":
            notification_list.append({
                "type": "info",
                "message": f" Your reservation is confirmed. {booking.room.room_type} • {booking.check_in} to {booking.check_out}. We’re delighted to host you."
            })

        # 🔴 Cancelled
        if booking.booking_status == "Cancelled":
            notification_list.append({
                "type": "danger",
                "message": f" Your booking for {booking.room.room_type} has been cancelled. We hope to welcome you again soon."
            })

        # 🟣 After Checkout
        if booking.check_out < today:
            notification_list.append({
                "type": "review",
                "message": f" Thank you for staying with us. We hope your moments here were truly special — we’d love to hear your thoughts.",
                "link": "/testimonial/"
            })

        notification_list = notification_list[::-1]

    return render(request, "restaurant/notifications.html", {
        "notifications": notification_list
    })