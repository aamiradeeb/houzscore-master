from django.contrib import admin
from django.urls import path, include  # Import the include function
from . import views

urlpatterns = [
     
    #path('', views.home_view, name='home'),  # The view for your home page


    #path('admin/', admin.site.urls),
    path('', include('analytics.urls')),  # Include your app's URLs here
]
