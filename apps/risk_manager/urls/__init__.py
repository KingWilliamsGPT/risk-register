from django.urls import path

from .. import views
app_name = 'risk_register'


urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('', views.Dashboard.as_view(), name='home'),

    path('risk/', views.AddRisk.as_view(), name='risk_create'),
    path('risk/<int:id>/', views.AddRisk.as_view(), name='risk_read'),
    path('risk/<int:id>/update', views.AddRisk.as_view(), name='risk_update'),
    path('risk/<int:id>/delete', views.AddRisk.as_view(), name='risk_delete'),

]
