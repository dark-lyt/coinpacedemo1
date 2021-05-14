from django.urls import path, include
from django.contrib.auth import views as auth_views
from account import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "account"

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('edit/', views.edit, name='edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.register, name='signup'),
    path('transactions/', views.transaction, name='transaction'),
    path('invest/', views.invest, name='invest'),
    # path('login/', views.login, name='login'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)