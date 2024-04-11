from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name= 'register'),
    path('login/', views.login_request, name='login_request'),
    path('upload/', views.image_upload, name='image_upload'),
    path('process/<str:image_name>/<str:language>/', views.model_process, name='model_process'), 
    path('logout/', views.logout, name='logout'),
    path('history/', views.history, name='history'),
    path('policy/', views.policy, name='policy'),
    path('contact-form/', views.contact_form, name='contact-form'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)