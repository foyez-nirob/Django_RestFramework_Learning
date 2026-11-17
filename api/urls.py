from django.urls import path,include
from . import views         # . -> represent current directory

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employee', views.EmployeeViewSet, basename='employee')       # that will automatic takecare of urls

urlpatterns = [
    path("student/", views.student_views),
    path("student/<int:pk>/", views.student_one_view),

    # path('Employee/', views.Employees.as_view()),    # as_view() to tell it's a class based views
    # path('Employee/<int:pk>/', views.Employee_one.as_view())

    path('', include(router.urls))
]