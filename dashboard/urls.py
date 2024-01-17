from django.urls import path
from dashboard import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'dashboard'

urlpatterns = [
    path('registration/',views.RegisterApi.as_view(), name='register_user'),
    path('login/',views.LoginView.as_view(), name='login_user'),
    path('logout/',views.LogoutView.as_view(), name='logout_user'),
    path('dashboard/',views.DashboardView.as_view(), name='dashboard'),
    path('tenant/<int:pk>/',views.TenantView.as_view(), name='tenant_details'),
    path('tenant/<int:pk>/search_units/',views.SearchView.as_view(), name='search_units'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)