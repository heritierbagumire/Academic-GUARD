from django.contrib import admin
from django.urls import path, include
from admin_app.views import admin_dashboard

urlpatterns = [
    path('admin/', include('admin_app.urls')),  # Custom admin_app URLs first
    path('admin/django/', admin.site.urls),     # Move default admin to a subpath
    path('', admin_dashboard),                  # Root URL
]