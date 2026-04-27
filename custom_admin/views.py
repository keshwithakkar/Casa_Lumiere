from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Testimonial, Amenity, FAQ, Gallery, ContactUs, ContactEnquiry, Restaurant, Room, Guest, Booking, Coupon, AdminUser, RegisteredUser, MenuItem
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from datetime import date

def dashboard(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    for booking in Booking.objects.all():
        if booking.booking_status == "Cancelled":
            continue
        elif booking.check_out < date.today():
            booking.booking_status = "Completed"
        else:
            booking.booking_status = "Confirmed"
        booking.save()

    total_amenities = Amenity.objects.count()
    total_enquiries = ContactEnquiry.objects.count()
    total_testimonials = Testimonial.objects.count()
    total_guests = Guest.objects.count()
    total_bookings = Booking.objects.count()
    total_rooms = Room.objects.count()
    total_registered_users = RegisteredUser.objects.count()

    # total revenue of confirmed and completed bookings
    total_revenue = Booking.objects.filter(
        booking_status__in=['Confirmed', 'Completed']
    ).aggregate(total=Sum('total_price'))['total'] or 0

    # ✅ Monthly Revenue
    monthly_data = (
        Booking.objects.filter(booking_status__in=['Confirmed', 'Completed'])
        .annotate(month=ExtractMonth('check_out'))
        .values('month')
        .annotate(total=Sum('total_price'))
        .order_by('month')
    )

    # Prepare list for 12 months
    months = [0] * 12
    for item in monthly_data:
        months[item['month'] - 1] = float(item['total'])

    context = {
        'total_amenities': total_amenities,
        'total_enquiries': total_enquiries,
        'total_testimonials': total_testimonials,
        'total_guests': total_guests,
        'total_bookings': total_bookings,
        'total_rooms': total_rooms,
        'total_registered_users': total_registered_users,
        'total_revenue': total_revenue,
        'monthly_revenue': months,  # 👈 ADD THIS
    }

    return render(request, 'custom_admin/dashboard.html', context)


def testimonials(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'custom_admin/testimonials.html', {
        'testimonials': testimonials
    })

def add_testimonial(request):
    if request.method == 'POST':
        Testimonial.objects.create(
            name=request.POST['name'],
            message=request.POST['message'],
            image=request.FILES['image']
        )
        return redirect('admin_testimonials')

    return render(request, 'custom_admin/add_testimonial.html')

def edit_testimonial(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)

    if request.method == "POST":
        testimonial.name = request.POST.get('name')
        testimonial.message = request.POST.get('message')

        if request.FILES.get('image'):
            testimonial.image = request.FILES.get('image')

        testimonial.save()
        return redirect('admin_testimonials')

    return render(request, 'custom_admin/edit_testimonial.html', {
        'testimonial': testimonial
    })

def delete_testimonial(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)
    testimonial.delete()
    return redirect('admin_testimonials')

def amenities(request):
    amenities = Amenity.objects.all()
    return render(request, 'custom_admin/amenities.html', {
        'amenities': amenities
    })


def add_amenity(request):
    if request.method == 'POST':
        Amenity.objects.create(
            name=request.POST['name'],
            category=request.POST['category'],
            image=request.FILES['image']
        )
        return redirect('admin_amenities')

    return render(request, 'custom_admin/add_amenity.html')

def edit_amenity(request, id):
    amenity = get_object_or_404(Amenity, id=id)

    if request.method == 'POST':
        amenity.name = request.POST['name']
        amenity.category = request.POST.get('category', amenity.category)

        if request.FILES.get('image'):
            amenity.image = request.FILES['image']

        amenity.save()
        return redirect('admin_amenities')

    return render(request, 'custom_admin/edit_amenity.html', {
        'amenity': amenity
    })

def delete_amenity(request, id):
    amenity = get_object_or_404(Amenity, id=id)
    amenity.delete()
    return redirect('admin_amenities')


def admin_faqs(request):
    faqs = FAQ.objects.all()
    return render(request, 'custom_admin/faq.html', {'faqs': faqs})

def admin_add_faq(request):
    if request.method == "POST":
        FAQ.objects.create(
            question=request.POST.get('question'),
            answer=request.POST.get('answer')
        )
        return redirect('admin_faqs')

    return render(request, 'custom_admin/add_faq.html')

def admin_edit_faq(request, id):
    faq = get_object_or_404(FAQ, pk=id)

    if request.method == "POST":
        faq.question = request.POST.get('question')
        faq.answer = request.POST.get('answer')
        faq.save()
        return redirect('admin_faqs')

    return render(request, 'custom_admin/edit_faq.html', {'faq': faq})

def admin_delete_faq(request, id):
    FAQ.objects.filter(pk=id).delete()
    return redirect('admin_faqs')


def admin_gallery(request):
    gallery_list = Gallery.objects.all()
    return render(request, 'custom_admin/gallery.html', {
        'gallery_list': gallery_list
    })


def add_gallery(request):
    if request.method == 'POST':
        Gallery.objects.create(
            category_name=request.POST.get('category_name'),
            image=request.FILES.get('image')
        )
        return redirect('admin_gallery')

    return render(request, 'custom_admin/add_gallery.html')


def edit_gallery(request, pk):
    gallery = Gallery.objects.get(pk=pk)

    if request.method == 'POST':
        gallery.category_name = request.POST.get('category_name')

        if request.FILES.get('image'):
            gallery.image = request.FILES.get('image')

        gallery.save()
        return redirect('admin_gallery')

    return render(request, 'custom_admin/edit_gallery.html', {
        'gallery': gallery
    })


def delete_gallery(request, pk):
    Gallery.objects.filter(pk=pk).delete()
    return redirect('admin_gallery')


def admin_contactus(request):
    contact = ContactUs.objects.first()
    return render(request, 'custom_admin/contactus.html', {'contact': contact})

def admin_edit_contactus(request):
    contact, created = ContactUs.objects.get_or_create(pk=1)

    if request.method == "POST":
        contact.description = request.POST.get('description')
        contact.save()
        return redirect('admin_contactus')

    return render(request, 'custom_admin/edit_contactus.html', {'contact': contact})

def admin_enquiries(request):
    enquiries = ContactEnquiry.objects.all().order_by('-enquiry_id')
    return render(request, 'custom_admin/enquiry.html', {
        'enquiries': enquiries
    })


# RESTAURANT LIST
def admin_restaurant(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'custom_admin/restaurant.html', {
        'restaurants': restaurants
    })

# ADD RESTAURANT
def admin_add_restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Restaurant.objects.create(
            name=name,
            description=description,
            image=image
        )
        return redirect('admin_restaurant')

    return render(request, 'custom_admin/add_restaurant.html')


# EDIT RESTAURANT
def admin_edit_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, restaurant_id=id)

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.description = request.POST.get('description')

        if request.FILES.get('image'):
            restaurant.image = request.FILES.get('image')

        restaurant.save()
        return redirect('admin_restaurant')

    return render(request, 'custom_admin/edit_restaurant.html', {'restaurant': restaurant})


# DELETE RESTAURANT
def admin_delete_restaurant(request, id):
    restaurant = get_object_or_404(Restaurant, restaurant_id=id)
    restaurant.delete()
    return redirect('admin_restaurant')


# LIST
def admin_rooms(request):
    rooms = Room.objects.all().order_by('id')
    return render(request, 'custom_admin/rooms.html', {'rooms': rooms})


# ADD
def admin_add_room(request):
    if request.method == "POST":
        room_type = request.POST.get('room_type')
        description = request.POST.get('description')
        price = request.POST.get('price')
        total_rooms = request.POST.get('total_rooms')
        image = request.FILES.get('image')

        Room.objects.create(
            room_type=room_type,
            description=description,
            price=price,
            total_rooms=total_rooms,
            image=image
        )

        return redirect('admin_rooms')

    return render(request, 'custom_admin/add_room.html')


# EDIT
def admin_edit_room(request, id):
    room = get_object_or_404(Room, id=id)

    if request.method == "POST":
        room.room_type = request.POST.get('room_type')
        room.description = request.POST.get('description')
        room.price = request.POST.get('price')
        room.total_rooms = request.POST.get('total_rooms')

        if request.FILES.get('image'):
            room.image = request.FILES.get('image')

        room.save()
        return redirect('admin_rooms')

    return render(request, 'custom_admin/edit_room.html', {'room': room})


# DELETE
def admin_delete_room(request, id):
    room = get_object_or_404(Room, id=id)
    room.delete()
    return redirect('admin_rooms')


# List Guests
def admin_guests(request):
    guests = Guest.objects.all()
    return render(request, 'custom_admin/guests.html', {'guests': guests})

# Add Guest
def admin_add_guest(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        Guest.objects.create(name=name, email=email, phone=phone)
        return redirect('admin_guests')
    return render(request, 'custom_admin/add_guest.html')

# Edit Guest
def admin_edit_guest(request, guest_id):
    guest = get_object_or_404(Guest, id=guest_id)
    if request.method == 'POST':
        guest.name = request.POST.get('name')
        guest.email = request.POST.get('email')
        guest.phone = request.POST.get('phone')
        guest.save()
        return redirect('admin_guests')
    return render(request, 'custom_admin/edit_guest.html', {'guest': guest})

# Delete Guest
def admin_delete_guest(request, guest_id):
    guest = get_object_or_404(Guest, id=guest_id)
    if request.method == 'POST':
        guest.delete()
        return redirect('admin_guests')
    return render(request, 'custom_admin/delete_guest.html', {'guest': guest})


# List all bookings
def admin_bookings(request):
    status = request.GET.get('status')

    bookings = Booking.objects.select_related('guest', 'room').all().order_by('id')

    # ✅ AUTO UPDATE STATUS
    for booking in bookings:
        if booking.booking_status == "Cancelled":
            continue
        elif booking.check_out < date.today():
            booking.booking_status = "Completed"
        else:
            booking.booking_status = "Confirmed"
        booking.save()

    # ✅ FILTER
    if status == "Confirmed":
        bookings = bookings.filter(booking_status="Confirmed")
    elif status == "Cancelled":
        bookings = bookings.filter(booking_status="Cancelled")
    elif status == "Completed":
        bookings = bookings.filter(booking_status="Completed")
    # if "all" or empty → show all

    return render(request, 'custom_admin/bookings.html', {
        'bookings': bookings,
        'selected_status': status
    })

# Add booking
def admin_add_booking(request):
    guests = Guest.objects.all()
    rooms = Room.objects.all().order_by('id')

    if request.method == 'POST':
        guest_id = request.POST['guest']
        room_id = request.POST['room']
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        adults = int(request.POST['adults'])
        children = int(request.POST['children'])
        rooms_booked = int(request.POST.get("rooms_booked", 1))
        room_price = float(request.POST['room_price'])
        extra_guest_price = float(request.POST['extra_guest_price'])
        tax_price = float(request.POST['tax_price'])
        discount_price = float(request.POST['discount_price'])
        total_price = float(request.POST['total_price'])
        coupon_code = request.POST.get('coupon_code', '')
        booking_status = request.POST.get("booking_status", "Confirmed")

        Booking.objects.create(
            guest_id=guest_id,
            room_id=room_id,
            check_in=check_in,
            check_out=check_out,
            adults=adults,
            children=children,
            rooms_booked=rooms_booked,
            room_price=room_price,
            extra_guest_price=extra_guest_price,
            tax_price=tax_price,
            discount_price=discount_price,
            total_price=total_price,
            coupon_code=coupon_code,
            booking_status=booking_status,
        )

        

        return redirect('admin_bookings')

    return render(request, 'custom_admin/add_booking.html', {'guests': guests, 'rooms': rooms})

# Edit booking
def admin_edit_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    guests = Guest.objects.all()
    rooms = Room.objects.all().order_by('id')

    if request.method == 'POST':
        old_status = booking.booking_status  # store old status before updating

        booking.guest_id = request.POST['guest']
        booking.room_id = request.POST['room']
        booking.check_in = request.POST['check_in']
        booking.check_out = request.POST['check_out']
        booking.adults = int(request.POST['adults'])
        booking.children = int(request.POST['children'])
        booking.rooms_booked = int(request.POST['rooms_booked'])
        booking.room_price = float(request.POST['room_price'])
        booking.extra_guest_price = float(request.POST['extra_guest_price'])
        booking.tax_price = float(request.POST['tax_price'])
        booking.discount_price = float(request.POST['discount_price'])
        booking.total_price = float(request.POST['total_price'])
        booking.coupon_code = request.POST.get('coupon_code', '')
        new_status = request.POST['booking_status']

        

        booking.booking_status = new_status
        booking.save()
        return redirect('admin_bookings')

    return render(request, 'custom_admin/edit_booking.html', {
        'booking': booking,
        'guests': guests,
        'rooms': rooms,
    })

# Delete booking
def admin_delete_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    room = booking.room

    

    booking.delete()
    return redirect('admin_bookings')


# List all coupons
def admin_coupon(request):
    coupons = Coupon.objects.all()
    return render(request, 'custom_admin/coupons.html', {'coupons': coupons})

# Add a new coupon
def admin_add_coupon(request):
    if request.method == 'POST':
        code = request.POST['code']
        percentage = request.POST['percentage']
        Coupon.objects.create(code=code, percentage=percentage)
        return redirect('admin_coupon')
    return render(request, 'custom_admin/add_coupon.html')

# Edit an existing coupon
def admin_edit_coupon(request, id):
    coupon = get_object_or_404(Coupon, id=id)
    if request.method == 'POST':
        coupon.code = request.POST['code']
        coupon.percentage = request.POST['percentage']
        coupon.save()
        return redirect('admin_coupon')
    return render(request, 'custom_admin/edit_coupon.html', {'coupon': coupon})

# Delete a coupon
def admin_delete_coupon(request, id):
    coupon = get_object_or_404(Coupon, id=id)
    coupon.delete()
    return redirect('admin_coupon')


def admin_login(request):
    error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            admin = AdminUser.objects.get(username=username, password=password)
            request.session['admin_id'] = admin.id
            return redirect('admin_dashboard')
        except AdminUser.DoesNotExist:
            error = "Invalid Username or Password"

    return render(request, "custom_admin/login.html", {"error": error})


def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')

def admin_profile(request):
    if not request.session.get('admin_id'):
        return redirect('admin_login')

    admin = AdminUser.objects.get(id=request.session['admin_id'])
    message = ""

    if request.method == "POST":
        new_username = request.POST.get("username")
        new_password = request.POST.get("password")

        admin.username = new_username

        if new_password:
            admin.password = new_password

        admin.save()
        message = "Profile Updated Successfully!"

    return render(request, "custom_admin/profile.html", {
        "admin": admin,
        "message": message
    })

# READ (List Users)
def admin_registered_users(request):

    if not request.session.get('admin_id'):
        return redirect('admin_login')

    users = RegisteredUser.objects.all().order_by('id')

    return render(request, 'custom_admin/registered_users.html', {
        'users': users
    })

# CREATE (Add User)
def admin_add_registered_user(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        RegisteredUser.objects.create(
            username=username,
            email=email,
            password=password
        )

        return redirect("admin_registered_users")

    return render(request, "custom_admin/add_registered_user.html")

# UPDATE (Edit User)
def admin_edit_registered_user(request, id):

    user = get_object_or_404(RegisteredUser, id=id)

    if request.method == "POST":

        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.password = request.POST.get("password")

        user.save()

        return redirect("admin_registered_users")

    return render(request, "custom_admin/edit_registered_user.html", {
        "user": user
    })

# DELETE (Delete User)
def admin_delete_registered_user(request, id):

    user = get_object_or_404(RegisteredUser, id=id)

    if request.method == "POST":
        user.delete()

    return redirect("admin_registered_users")


def admin_menu(request):
    items = MenuItem.objects.all()
    return render(request, "custom_admin/menu.html", {"items": items})

def admin_add_menu(request):

    restaurants = Restaurant.objects.all()

    if request.method == "POST":
        restaurant_id = request.POST.get("restaurant")
        item_name = request.POST.get("item_name")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        MenuItem.objects.create(
            restaurant_id=restaurant_id,
            item_name=item_name,
            description=description,
            image=image
        )

        return redirect("admin_menu")

    return render(request, "custom_admin/add_menu.html", {
        "restaurants": restaurants
    })

def admin_edit_menu(request, id):

    item = get_object_or_404(MenuItem, id=id)
    restaurants = Restaurant.objects.all()

    if request.method == "POST":

        item.restaurant_id = request.POST.get("restaurant")
        item.item_name = request.POST.get("item_name")
        item.description = request.POST.get("description")

        if request.FILES.get("image"):
            item.image = request.FILES.get("image")

        item.save()

        return redirect("admin_menu")

    return render(request, "custom_admin/edit_menu.html", {
        "item": item,
        "restaurants": restaurants
    })

def admin_delete_menu(request, id):

    item = get_object_or_404(MenuItem, id=id)
    item.delete()

    return redirect("admin_menu")