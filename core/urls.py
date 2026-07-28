from django.urls import path
from core import views

urlpatterns = [
    # Portals
    path('', views.store, name='store_front'),
    path('admin-portal/', views.index, name='admin_portal'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('customer-portal/', views.customer_portal, name='customer_portal'),
    path('signup/', views.signup_view, name='signup'),
    
    # APIs
    path('api/state', views.api_state, name='api_state'),
    path('api/barcode/<str:sku>/', views.generate_barcode, name='generate_barcode'),
    path('api/qrcode/<str:sku>/', views.generate_qrcode, name='generate_qrcode'),
    path('api/export/excel/', views.export_excel, name='export_excel'),
    path('api/export/pdf/', views.export_pdf, name='export_pdf'),
]
