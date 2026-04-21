from django.urls import path
from . import views

urlpatterns = [
    path('', views.consulta_view, name='inicio'),
    path('reservar/gracias/', views.consulta_exitosa, name='consulta_exitosa'),

    # Panel
    path('panel/login/', views.panel_login, name='panel_login'),
    path('panel/logout/', views.panel_logout, name='panel_logout'),
    path('panel/', views.panel, name='panel'),
    path('panel/<int:pk>/', views.panel_detalle, name='panel_detalle'),
    path('panel/<int:pk>/editar/', views.panel_editar, name='panel_editar'),
    path('panel/<int:pk>/borrar/', views.panel_borrar, name='panel_borrar'),
    path('panel/<int:pk>/etiqueta/', views.panel_etiqueta, name='panel_etiqueta'),
]