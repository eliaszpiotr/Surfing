from django.urls import path
from guide import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create_surf_spot/', views.CreateSurfSpotView.as_view(), name='create_surf_spot'),
    path('spots_list/', views.SpotsListView.as_view(), name='spots_list'),
    path('login_register/', views.LoginRegisterView.as_view(), name='login_register'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
