from django.shortcuts import render, redirect, get_object_or_404
from .forms import TrackingCodeForm
from .models import Package, Customer, TrackingCode


def package_detail(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    return render(request, 'package_detail.html', {'package': package})

def track_package(request):
    if request.method == 'POST':
        form = TrackingCodeForm(request.POST)
        if form.is_valid():
            tracking_code = form.cleaned_data['tracking_code']
            try:
                package = Package.objects.get(tracking_code__tracking_code=tracking_code)
                return redirect('consignment:package_detail', package_id=package.id)
            except Package.DoesNotExist:
                error_message = "Package with this tracking code does not exist."
                return render(request, 'track_package.html', {'form': form, 'error_message': error_message})
    else:
            form = TrackingCodeForm()

    context = {
            'form': form,
        }
    return render(request, 'track_package.html', context)


def package_detail(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    if request.method == "GET":
#       pdf = Package.objects.get(pdf=pdf)
     return render(request, 'package_detail.html', {'package': package})
