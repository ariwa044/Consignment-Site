import random
import string
from django.db import models
from django.core.mail import send_mail, EmailMessage, get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def generate_tracking_code():
    # Start with 'CB' for Tracking
    start_letters = 'CB'
    # Generate random digits for middle section
    middle_digits = ''.join(random.choices(string.digits, k=14))
    
    tracking_code = f"{start_letters}{middle_digits}"
    
    # Check if tracking code already exists and regenerate if needed
    while Package.objects.filter(tracking_code=tracking_code).exists():
        middle_digits = ''.join(random.choices(string.digits, k=14))
        tracking_code = f"{start_letters}{middle_digits}"
    
    return tracking_code

def generate_package_id():
    # Start with 'EXP' for Package
    start_letters = 'EXP'
    # Generate random digits for middle section
    middle_digits = ''.join(random.choices(string.digits, k=4))
    
    package_id = f"{start_letters}_{middle_digits}"
    
    # Check if package ID already exists and regenerate if needed
    while Package.objects.filter(package_id=package_id).exists():
        middle_digits = ''.join(random.choices(string.digits, k=5))
        package_id = f"{start_letters}_{middle_digits}"
    
    return package_id

class Package(models.Model):
    tracking_code = models.CharField(
        max_length=32, 
        unique=True,
        default=generate_tracking_code,
        editable=True  # Makes it editable in admin
    )
    package_id = models.CharField(max_length=20, default=generate_package_id, unique=True)
    package_name = models.CharField(max_length=100)
    sender = models.CharField(max_length=100, null=True, blank=True)
    receiver = models.CharField(max_length=100, null=True, blank=True)
    tel = models.CharField(max_length=15, null=True, blank=True, help_text='receiver phone number')
    email = models.EmailField(max_length=100, null=True, blank=True, help_text='receiver email address')
    sending_location = models.CharField(max_length=100, null=True, blank=True, help_text='sender address & city')
    receiving_location = models.CharField(max_length=100, null=True, blank=True, help_text='receiver address & city')
    current_location = models.CharField(max_length=300, null=True, blank=True, help_text='name for map iframe')
    package_description = models.TextField(null=True, blank=True)



    MODE_OF_TRANSIT_CHOICES = [
        ('Air', 'Air'),
        ('Sea', 'Sea'),
        ('Road', 'Road')
    ]
    mode_of_transit = models.CharField(max_length=10, choices=MODE_OF_TRANSIT_CHOICES)

    PACKAGE_STATUS_CHOICES = [
        ('Shipment Processed', 'Shipment Processed'),
        ('In Transit', 'In Transit'),
        ('Awaiting Customs Clearance', 'Awaiting Customs Clearance'),
        ('Customs Cleared', 'Customs Cleared'),
        ('At Destination Facility', 'At Destination Facility'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Returned', 'Returned'),
        ('Cancelled', 'Cancelled')
    ]
    package_status = models.CharField(max_length=32, choices=PACKAGE_STATUS_CHOICES)
    delivery_update = models.TextField(null=True, blank=True)
    #package_image = models.ImageField(upload_to='package_images/', default='default_image.jpg')
    package_weight = models.FloatField(null=True, blank=True, default=0.0)
    shipping_cost = models.FloatField(null=True, blank=True, default=0.0)
    package_quantity = models.IntegerField(default=1)

    shipping_date = models.DateField(auto_now=True, null=True, blank=True)
    delivery_date = models.DateField(auto_now_add=True, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Packages'

        
    def send_package_email(self):
        """Send email notification with tracking information using EmailMultiAlternatives"""
        import logging
        logger = logging.getLogger(__name__)
        
        if not self.email:
            logger.warning(f"No email address provided for package {self.package_id}")
            return False
    
        subject = "Your Package Shipment Confirmation"
        context = {
            'tracking_code': self.tracking_code,
            'destination': self.receiving_location,
            'current_location': self.current_location,
            'package': self
        }
    
        try:
            text_content = render_to_string('emails/package_notification.txt', context)
            html_content = render_to_string('emails/package_notification.html', context)
        except Exception as template_error:
            logger.error(f"Template rendering failed for package {self.package_id}: {str(template_error)}")
            return False
    
        try:
            # Create the email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[self.email],
                connection=get_connection()
            )
            # Attach HTML content
            email.attach_alternative(html_content, "text/html")
            # Send the email
            email.send()
            logger.info(f"Email sent using EmailMultiAlternatives for package {self.package_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to send package email via EmailMultiAlternatives: {str(e)}")
            return False

    def __str__(self):
        return f'{self.package_name} ({self.package_id}) '