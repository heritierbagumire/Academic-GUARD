from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', include('admin_app.urls')),
    path('student/', include('student_app.urls')),
    path('teacher/', include('teacher_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
