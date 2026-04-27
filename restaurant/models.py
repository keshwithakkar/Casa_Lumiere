from django.db import models


class amenities(models.Model):
    CATEGORY_CHOICES = [
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='amenities/')
    description = models.TextField(blank=True)


class about(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='about/')


class contact(models.Model):
    description = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)


class faq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


class gallery(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')


class terms(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content[:50]


class Testimonial(models.Model):
    name = models.CharField(max_length=150)
    message = models.TextField()
    image = models.ImageField(upload_to='testimonial/')
    
    def __str__(self):
        return self.name