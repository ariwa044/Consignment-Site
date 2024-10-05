from django.db import models


class Ship(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)  # Corrected 'true' to 'True'
    location = models.URLField(max_length=300, null=True, blank=True, help_text='URL for map iframe')

    class Meta:
        verbose_name = 'Ship'
        verbose_name_plural = 'Ships'

    def __str__(self):
        return f'Shipping for Package ({self.pk})'


class Customer(models.Model):
    customer_name = models.CharField(max_length=100, blank=False, null=False)
    customer_address = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=100)
    customer_email = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.customer_name


class Package(models.Model):
    tracking_code = models.CharField(max_length=100, unique=True)
    package_id = models.CharField(max_length=100, unique=True)
    package_name = models.CharField(max_length=100)
    package_weight = models.FloatField(null=True, blank=True, default=0.0)

    MODE_OF_TRANSIT_CHOICES = [
        ('Air', 'Air'),
        ('Sea', 'Sea'),
        ('Road', 'Road')
    ]
    mode_of_transit = models.CharField(max_length=10, choices=MODE_OF_TRANSIT_CHOICES)

    PACKAGE_STATUS_CHOICES = [
        ('Delivered', 'Delivered'),
        ('In Transit', 'In Transit')
    ]
    package_status = models.CharField(max_length=20, choices=PACKAGE_STATUS_CHOICES)

    sending_location = models.ForeignKey(
        Ship,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='send_location'
    )
    receiving_location = models.ForeignKey(
        'Ship',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='receive_location'
    )
    package_date = models.DateTimeField(auto_now_add=True)
    package_location = models.CharField(max_length=100)
    package_destination = models.CharField(max_length=100)
    sender = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sender'
    )
    receiver = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='receiver'
    )
    package_description = models.TextField(null=True, blank=True)
    package_quantity = models.IntegerField(default=1)
    pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Packages'

    def __str__(self):
        return f'{self.package_name} ({self.package_id})'
