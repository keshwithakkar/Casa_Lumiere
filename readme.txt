do booking table and add room number

restaurant table

restaurant_id
name
description
image


amenities table

amenity_id
name
category
image


aboutus

aboutus_id
title
description
image


contactus

contactus_id
description
name
email
phone


faq

faq_id
question
answer


gallery

category_name
image id
image


terms

id
content


testimonials

id
name
message
image



casa_lumiere
	casa_lumiere
		pycache
		init.py
		asgi.py
		settings.py
		urls.py
		wsgi.py
	custom_admin
		pycache
		migrations
		static
			custom_admin
				css
					admin.css
				images
		templates
			custom_admin
				add_amenity.html
				amenities.html
				base.html
				edit_amenity.html
				and crud for more modules like booking, coupon, faq, gallery, guest, restaurant, room, testimonial and contactus, dashboard
		init.py
		admin.py
		apps.py
		models.py
		tests.py
		urls.py
		views.py
	media
		testimonial
			person4.png
		gallery
			gal.png
		and more
	restaurant
		pycache
		migrations
		templates
			restaurant
				about.html
				amenities.html
				book.html
				contact.html
				faq.html
				gallery.html
				restaurant.html
				rooms.html
				terms.html
				testimonials.html
			home.html
		admin.py
		apps.py
		models.py
		urls.py
		views.py
	static
		restaurant
			css
				about.css
				amenities.css
				book.css
				contact.css
				faq.css
				gallery.css
				home.css
				restaurant.css
				rooms.css
				terms.css
				testimonials.css
			images
				multiple images with .png extension
	db.sqlite3
	manage.py
	readme.txt



rooms table

id
room_type
description
price
total_rooms
image


guest

id
name
email
phone


booking

id
guest_id
room_id
check_in and out date
adult and child
room_price
extra_guest_price
tax_price
discount_price
total_price
coupon_code
booking_status


coupon

id
code
percentage