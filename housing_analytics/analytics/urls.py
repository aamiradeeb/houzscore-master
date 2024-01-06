from django.urls import path
from . import views  

from django.conf.urls.static import static
from django.conf import settings


app_name = 'analytics'

urlpatterns = [
 
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('property_cma/', views.property_cma, name='property_cma'),
    path('ai_home_advisor/', views.ai_home_advisor, name='ai_home_advisor'),
    path('housing_analytic_report/', views.housing_analytic_report, name='housing_analytic_report'),
    path('score/', views.score, name='score'),
    path('about/', views.about, name='about'),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)