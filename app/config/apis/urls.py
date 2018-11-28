from django.urls import path, include

urlpatterns = [
    path('members/', include('members.apis.urls')),
    path('use-point/', include('use_point.apis.urls')),
    path('cashes/', include('cashes.apis.urls')),
    path('giftcards/', include('giftcard.apis.urls')),
    path('event/', include('event.apis.urls')),
    path('posts/', include('posts.apis.urls')),
]