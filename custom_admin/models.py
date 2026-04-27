from django.db import models
from django.contrib.auth.models import User

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    image = models.ImageField(upload_to='testimonial/')

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='amenities/')

    def __str__(self):
        return self.name

class FAQ(models.Model):
    faq_id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

class Gallery(models.Model):
    image_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='gallery/')

    def __str__(self):
        return self.category_name

class ContactUs(models.Model):
    description = models.TextField()

    def __str__(self):
        return f"Contact Content {self.contactus_id}"

class ContactEnquiry(models.Model):
    enquiry_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='restaurant_images/')

    def __str__(self):
        return self.name

class Room(models.Model):

    ROOM_TYPES = [
        ('Casa Suite', 'Casa Suite'),
        ('Deluxe', 'Deluxe'),
        ('Executive', 'Executive'),
    ]

    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_rooms = models.IntegerField()
    image = models.ImageField(upload_to='rooms/')

    def __str__(self):
        return self.room_type

class Guest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey("RegisteredUser", on_delete=models.CASCADE, null=True, blank=True)  # 👈 ADD THIS

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    check_in = models.DateField()
    check_out = models.DateField()

    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)

    rooms_booked = models.PositiveIntegerField(default=1)

    room_price = models.DecimalField(max_digits=10, decimal_places=2)
    extra_guest_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.guest.name} - {self.room.room_type} ({self.check_in} to {self.check_out})"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 15.00 for 15%

    def __str__(self):
        return f"{self.code} - {self.percentage}%"


class AdminUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class RegisteredUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class MenuItem(models.Model):

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="menu_items"
    )

    item_name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="menu_items/")

    def __str__(self):
        return self.item_name