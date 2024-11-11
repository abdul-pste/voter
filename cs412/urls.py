from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mini_fb/', include('mini_fb.urls')),
    path('voters/', include('voter_analytics.urls')),
    path('', RedirectView.as_view(url='voters/')),
]
