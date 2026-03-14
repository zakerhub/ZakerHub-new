"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customizing Admin Texts
admin.site.site_header = "ZakerHub Administration"
admin.site.site_title = "ZakerHub Admin"
admin.site.index_title = "Welcome to ZakerHub Portal"

# Customizing Admin Ordering
original_get_app_list = admin.AdminSite.get_app_list

def get_app_list(self, request, app_label=None):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    app_list = original_get_app_list(self, request, app_label)
    
    # Reorder models in 'academics' app
    ordering = {
        'Curriculum': 1,
        'Subject': 2, 
        'Course': 3,
        'Level': 4,
        'CourseItem': 5
    }
    
    for app in app_list:
        if app['app_label'] == 'academics':
            app['models'].sort(key=lambda x: ordering.get(x['object_name'], 99))
    
    return app_list

admin.AdminSite.get_app_list = get_app_list

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Version 1
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/academics/', include('academics.urls')),
    path('api/v1/subscriptions/', include('subscriptions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
