"""Anka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from school import views

router = routers.DefaultRouter()
router.register(r'teachers', views.TeacherViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'students', views.StudentViewSet)
router.register(r'courseworkers', views.CourseWorkerViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'login', views.LogInViewSet, basename='login')
router.register(r'check_attendance', views.CheckAttendanceViewSet,
                basename='check_attendance')
router.register(r'create_entities', views.CreateEntitiesViewSet,
                basename='create_entities')
router.register(r'attendances', views.AttendanceViewSet)
router.register(r'export_attendance',
                views.ExportAttendanceViewSet, basename='export_attendance')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
