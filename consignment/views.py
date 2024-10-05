from django.shortcuts import render, redirect, get_object_or_404
from .models import Package, Customer, Ship




#def index(request):
 #   return render (request, 'index.html')


def package_detail(request, package_id):
    # Retrieve the package object using the package_id
    package = get_object_or_404(Package, package_id=package_id)  # Use package_id instead of the default id

    # Prepare additional context
    context = {
        'package': package,
        'sender': package.sender,  # Get sender details
        'receiver': package.receiver,  # Get receiver details
        'sending_location': package.sending_location,  # Get sending location details
        'receiving_location': package.receiving_location,  # Get receiving location details
    }

    return render(request, 'package_detail.html', context)

#@cache_page(60 * 15)
def track_package(request):
    if request.method == 'POST':
        tracking_code = request.POST.get('tracking_code')  # Get the tracking code from the POST data
        if tracking_code:
            try:
                # Retrieve the package using the provided tracking code
                package = Package.objects.get(tracking_code=tracking_code)
                return redirect('consignment:package_detail', package_id=package.package_id)  # Use package_id correctly
            except Package.DoesNotExist:
                error_message = "Package with this tracking code does not exist."
                return render(request, 'index.html', {'error_message': error_message})
    else:
        return render(request, 'index.html')
