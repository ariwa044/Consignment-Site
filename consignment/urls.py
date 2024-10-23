from django.urls import path
from . import views

app_name = 'consignment'

urlpatterns = [
    path('', views.track_package, name='track_package'),
    #path('track/', views.track_package, name='track_package'),
    path('package/<str:package_id>/', views.package_detail, name='package_detail'),
    path('receipt/<str:package_id>/', views.generate_pdf, name='generate_receipt'),
]
