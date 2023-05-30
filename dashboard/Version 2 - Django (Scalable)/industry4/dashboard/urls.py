from django.urls import path

# Importing views
from . import views

# Importing static and settings to serve media files - for local development only
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    # path('init_input', views.initial_input, name="initial_input"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


