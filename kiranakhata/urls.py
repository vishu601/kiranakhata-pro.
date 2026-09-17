from django.contrib import admin
from django.urls import path
from ledger import views as ledger_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 🏢 Master Admin Core
    path('admin/', admin.site.urls),
    
    # 🔒 Dukandaar Authentication Engine (Login / Logout)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # 🏪 Custom Kirana Registration & Main Dashboard
    path('signup/', ledger_views.signup_view, name='signup'),
    path('dashboard/', ledger_views.dashboard_view, name='dashboard'),
    
    # 🏠 Landing Route Launcher (Direct open karne par automatic dashboard par le jayega)
    path('', ledger_views.dashboard_view, name='home'), 
]