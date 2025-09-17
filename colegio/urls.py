from django.urls import path
from . import views

urlpatterns = [
    # URL para la página principal
    path('', views.home_view, name='home'),

    # URLs para Area
    path('areas/', views.AreaListView.as_view(), name='area-list'),
    path('areas/create/', views.AreaCreateView.as_view(), name='area-create'),
    path('areas/<int:pk>/update/', views.AreaUpdateView.as_view(), name='area-update'),
    path('areas/<int:pk>/delete/', views.AreaDeleteView.as_view(), name='area-delete'),
    
    # URLs para Oficina
    path('oficinas/', views.OficinaListView.as_view(), name='oficina-list'),
    path('oficinas/create/', views.OficinaCreateView.as_view(), name='oficina-create'),
    path('oficinas/<int:pk>/update/', views.OficinaUpdateView.as_view(), name='oficina-update'),
    path('oficinas/<int:pk>/delete/', views.OficinaDeleteView.as_view(), name='oficina-delete'),
    
    # URLs para SalonClase
    path('salones/', views.SalonClaseListView.as_view(), name='salonclase-list'),
    path('salones/create/', views.SalonClaseCreateView.as_view(), name='salonclase-create'),
    path('salones/<int:pk>/update/', views.SalonClaseUpdateView.as_view(), name='salonclase-update'),
    path('salones/<int:pk>/delete/', views.SalonClaseDeleteView.as_view(), name='salonclase-delete'),
    
    # URLs para Persona
    path('personas/', views.PersonaListView.as_view(), name='persona-list'),
    path('personas/create/', views.PersonaCreateView.as_view(), name='persona-create'),
    path('personas/<int:pk>/update/', views.PersonaUpdateView.as_view(), name='persona-update'),
    path('personas/<int:pk>/delete/', views.PersonaDeleteView.as_view(), name='persona-delete'),

        # URL para el reporte
    path('reporte-areas/', views.ReporteAreaView.as_view(), name='reporte-area'),

        # URL para exportar reporte a PDF
    path('exportar-reporte-pdf/', views.exportar_reporte_pdf, name='exportar-reporte-pdf'),
]