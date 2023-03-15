from django.urls import path
from guide import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create_surf_spot/', views.CreateSurfSpotView.as_view(), name='create_surf_spot'),
    path('spots_list/', views.SpotsListView.as_view(), name='spots_list'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
