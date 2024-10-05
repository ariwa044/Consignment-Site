from django.contrib import admin
from .models import Customer, Package, Ship


class PackageAdmin(admin.ModelAdmin):
    list_display = (
        'package_id', 'package_name', 'package_weight', 'mode_of_transit',
        'tracking_code',
        'package_status', 'package_date', 'package_location',
        'package_destination', 'sender', 'receiver', 'package_description',
        'package_quantity', 'pdf'
    )
    search_fields = ('package_id', 'package_name', 'tracking_code')
    list_filter = ('package_status', 'mode_of_transit', 'package_date')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_address', 'customer_phone', 'customer_email')
    search_fields = ('customer_name', 'customer_email', 'customer_phone')
    list_filter = ('customer_address',)


class ShipAdmin(admin.ModelAdmin):
    list_display = ('title', 'location')
    search_fields = ('title','location')

    # Custom display for map iframes in the admin panel
    def map_iframe(self, obj):
        iframe_html = ''
        if obj.sending_location:
            iframe_html += f'<iframe src="{obj.sending_location}" width="300" height="200"></iframe>'
        if obj.receiving_location:
            iframe_html += f'<iframe src="{obj.receiving_location}" width="300" height="200"></iframe>'
        return iframe_html or "No Map URLs Provided"

    map_iframe.short_description = 'Map Preview'
    map_iframe.allow_tags = True
    readonly_fields = ('map_iframe',)


admin.site.register(Package, PackageAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Ship, ShipAdmin)
