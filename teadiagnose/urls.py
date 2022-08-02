"""teadiagnose URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from .admin import admin_site
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from imgUp import views 
from iBp.views import ibpinterface

admin.site.site_header = 'TeaDiag - Administration'
admin.site.site_title = 'TeaDiagAdmin'
admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('demopage/', showDemo),
    path('descript/<str:f>/', views.showHtml),
    path('iBpInterface/', ibpinterface),
    #----------------------------------------------
    path('', views.main, name='home'),
    path('show/<img_id>/', views.showImg, name='show_image'),
    path('upload/', views.uploadImg, name='upload'),
    path('region/', views.add_region, name='add_region'),
    path('history/', views.showHistory, name='get_history'),
    path('feedback/', views.feedback, name='send_feedback'),
    path('error/<issue>/', views.errorpage, name='error'),
    path('mailtest/', views.errorpage, name='mailtest'),
    path('loadcities/', views.load_cities, name='ajax_load_cities'),
    path('tealinebot/', include('tealinebot.urls')),
    # ------------------------------------------------
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

