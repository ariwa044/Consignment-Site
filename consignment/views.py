import logging
import os
import tempfile

from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from .pdf import generate_receipt_pdf

from .models import Package

# Set up logging
logger = logging.getLogger(__name__)

# Set your ConvertAPI secret key
CONVERTAPI_SECRET = 'secret_TvNBjlPVoRE8F5oN'

def package_detail(request, package_id):
    try:
        package = get_object_or_404(Package, package_id=package_id)
        context = {
            'package': package,
            'sender': package.sender,
            'receiver': package.receiver,
            'sending_location': package.sending_location,
            'receiving_location': package.receiving_location,
        }
        return render(request, 'package_detail.html', context)
    except Exception as e:
        logger.error(f"Error in package_detail view: {e}")
        return HttpResponseServerError("An error occurred while retrieving package details.")

def track_package(request):
    if request.method == 'POST':
        tracking_code = request.POST.get('tracking_code')
        if tracking_code:
            try:
                package = Package.objects.filter(tracking_code=tracking_code).first()
                if package:
                    return redirect('consignment:package_detail', package_id=package.package_id)
                else:
                    error_message = "Package with this tracking code does not exist."
                    return render(request, 'index.html', {'error_message': error_message})
            except Exception as e:
                logger.error(f"Error in track_package view: {e}")
                return HttpResponseServerError("An error occurred while tracking the package.")
    return render(request, 'index.html')

def generate_pdf(request, package_id):
    # Create a new HTTP response with PDF content type
    response = HttpResponse(content_type='application/pdf')

    # Set Content-Disposition to 'inline' to render the PDF in the browser
    response['Content-Disposition'] = f'inline; filename="package_receipt_{package_id}.pdf"'

    # Get the Package object
    package = get_object_or_404(Package, package_id=package_id)

    # Call the function from pdf.py to generate the receipt
    generate_receipt_pdf(response, package)

    # Return the generated PDF as the response (will be displayed in browser)
    return response
