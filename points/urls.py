from django.urls import path
from . import views

app_name = 'points'

urlpatterns = [
    path('', views.point_list, name='point_list'),
    path('new/', views.point_create, name='point_create'),
    path('<int:pk>/edit/', views.point_edit, name='point_edit'),
    path('import/', views.import_points, name='import_points'),
    path('analysis/', views.point_analysis, name='point_analysis'),
    path('calculator/', views.coordinate_calculator,
         name='coordinate_calculator'),
    path('<int:pk>/delete/', views.point_delete, name='point_delete'),
]
