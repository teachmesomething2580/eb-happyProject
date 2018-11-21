from django.urls import path, include

urlpatterns = [
    path('members/', include('members.apis.urls')),
    path('use-point/', include('use_point.apis.urls')),
]