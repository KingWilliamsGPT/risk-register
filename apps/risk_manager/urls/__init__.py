from django.urls import path

from apps.risk_manager.views import RiskStat
from .. import views
app_name = 'risk_register'


urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('', views.Dashboard.as_view(), name='home'),

    path('risk/', views.RiskListView.as_view(), name='risk_list'),
    path('risk/add/', views.AddRisk.as_view(), name='risk_create'),
    path('risk/<int:id>/', views.AddRisk.as_view(), name='risk_read'),
    path('risk/<int:id>/update', views.AddRisk.as_view(), name='risk_update'),
    path('risk/<int:id>/delete', views.AddRisk.as_view(), name='risk_delete'),
    path('risk/statistics/', views.RiskStat.as_view(), name='risk_statistics'),
    path('risk/statistics/api/data/pie_for_risk_summary/', views.RiskPieSummary.as_view(), name='risk_pie_summary'),
    path('risk/pinned/', views.RiskPinned.as_view(), name='risk_pinned'),

]
