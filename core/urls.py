
from django.urls import path, include
from core.views import contact, home, price, about, terms, services
from django.conf.urls.static import static
from django.conf import settings


app_name = "core"
urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('services/', services, name="services"),
    path('price/', price, name="price"),
    path('contact/', contact, name="contact"),
    path('termsandconditions/', terms, name="terms"),
    # path('signup/', signup, name="signup"),

] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)