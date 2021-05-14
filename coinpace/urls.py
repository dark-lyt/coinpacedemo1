from coinpace.settings import STATIC_ROOT, STATIC_URL
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from cryptocurrency_payment import urls as cryptocurrency_payment_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls", namespace='core')),
    path('', include('django.contrib.auth.urls')),
    path('account/', include("account.urls", namespace='account')),
    path('paydetails/', include(cryptocurrency_payment_urls)),
] + static(STATIC_URL, document_root=STATIC_ROOT)
 
