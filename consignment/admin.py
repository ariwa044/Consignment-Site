from django.contrib import admin
from .models import TrackingCode, Customer, Package, Ship


class TrackingCodeAdmin(admin.ModelAdmin):
  list_display = ('tracking_code', )


class PackageAdmin(admin.ModelAdmin):
  list_display = ('package_id', 'package_name', 'package_weight',
                  'mode_of_transit', 'package_status', 'package_date',
                  'package_location', 'package_destination',
                   'sender',
                  'receiver', 'package_description', 'package_quantity', 'pdf')

class CustomerAdmin(admin.ModelAdmin):
  list_display = (
      'customer_name',
      'customer_address',
      'customer_phone',
      'customer_email',
  )


class ShipAdmin(admin.ModelAdmin):
  list_display = ('sending_location', 'receiving_location')


admin.site.register(Package, PackageAdmin)
admin.site.register(TrackingCode, TrackingCodeAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Ship, ShipAdmin)

# Register your models here.
