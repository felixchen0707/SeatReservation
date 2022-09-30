from django.urls import path

from UserAuth import views

urlpatterns = [
    path('login/<int:nid>/', views.register_and_login),
    path('logout/', views.logout),
    path('verify/', views.generate_verification_code)
]
