from django.urls import path, include

urlpatterns = [
    path('members/', include('members.apis.urls'))
]