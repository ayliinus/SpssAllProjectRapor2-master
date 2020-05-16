from django.conf.urls import include, url
from django.contrib import admin
from webProject import views



urlpatterns = [

   url(r'^admin/', admin.site.urls),
   url(r'^', include('contact.urls')),
   url(r'^accounts/', include('django.contrib.auth.urls')),
   url(r'^$', views.HomePageView.as_view(), name='home'),
   url(r'^calisanlar/$', views.tum_calisanlar),
   url(r'^calisan/,(?P<calisan_no>[-\w]+)/$', views.calisan_detay),
   url(r'^yoneticiler/$', views.tum_yoneticiler),
   url(r'^yonetici/,(?P<yonetici_no>[-\w]+)/$', views.yonetici_detay),
   url(r'^planlar/$', views.tum_planlar),
   url(r'^plan/,(?P<plan_no>[-\w]+)/$', views.plan_detay),
   url(r'^mekanlar/$', views.tum_mekanlar),
   url(r'^mekan/,(?P<mekan_no>[-\w]+)/$/', views.mekan_detay),
   url(r'^GirisSayfasi/$', views.GirisSayfasi.as_view()),
   url(r'^GirisSayfasi/ProfilSayfasi/$', views.ProfilSayfasi.as_view()),
   url(r'^GirisSayfasi/ProfilSayfasi/CalimaPlani/$', views.CalimaPlani.as_view()),
   url(r'^GirisSayfasi/ProfilSayfasi/CalimaPlani/GirisSayfasi/$', views.GirisSayfasi.as_view()),
   url(r'^GirisSayfasi/ProfilSayfasi/GecmisCalismaPlani/$', views.GecmisCalismaPlani.as_view()),
   url(r'^GirisSayfasi/ProfilSayfasi/CalismaPlani/GecmisShift/$', views.GecmisShift.as_view()),
   url(r'^GirisSayfasi/ProfilSayfasi/İstekYap/$', views.İstekYap.as_view()),
   url(r'^GirisSayfasi/ProfilSayfasi/DegisiklikTalebi/$', views.DegisiklikTalebi.as_view()),
   url(r'^GirisSayfasi/ProfilSayfasi/İstekYap/IstekYapSec/$', views.IstekYapSec.as_view()),

]




