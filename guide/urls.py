from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from guide import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('user_profile_form/', views.UserProfileFormView.as_view(), name='user_profile_form'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('create_surf_spot/', views.CreateSurfSpotView.as_view(), name='create_surf_spot'),
    path('spots_list/', views.SpotsListView.as_view(), name='spots_list'),
    path('user_profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    path('surf_spot/<int:pk>/', views.SurfSpotView.as_view(), name='surf_spot'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
