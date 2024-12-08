from django.urls import path

from apps.risk_manager.views import RiskStat
from .. import views


app_name = 'risk_register'


urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('', views.Dashboard.as_view(), name='home'),

    # this also shouldn't be here, but again kinda lazy 

    path('me/password_change/', views.MePasswordChange.as_view(), name='password_change'),
    path('me/recovery_codes/reset', views.MeRecoveryCodeReset.as_view(), name='recovery_codes_reset'),
    path('me/recovery_codes/download', views.MeRecoveryCodeDownload.as_view(), name='recovery_codes_download'),

    path('risk/', views.RiskListView.as_view(), name='risk_list'),
    path('risk/excel/', views.DownloadRiskExcel.as_view(), name='risk_excel'),
    path('risk/add/', views.AddRisk.as_view(), name='risk_create'),
    path('risk/<int:pk>/', views.AddRisk.as_view(), name='risk_read'),
    path('risk/<int:pk>/update/', views.RiskDetailView.as_view(), name='risk_update'),
    path('risk/<int:pk>/update/editors_list/', views.RiskEditors.as_view(), name='risk_editors'),
    path('risk/<int:pk>/delete/', views.RiskDeleteView.as_view(), name='risk_delete'),
    path('risk/statistics/', views.RiskStat.as_view(), name='risk_statistics'),
    path('risk/statistics/api/data/pie_for_risk_summary/', views.RiskPieSummary.as_view(), name='risk_type_summary'),
    path('risk/statistics/api/data/pie_for_risk_rating_summary/', views.RiskRatingSummary.as_view(), name='risk_rating_summary'),
    path('risk/statistics/api/data/super_summary/', views.RiskSuperSummaryView.as_view(), name='risk_super_summary'),
    path('risk/statistics/api/data/severe_risk_summary/', views.RiskSeveritySummaryView.as_view(), name='risk_severe_summary'),
    path('risk/statistics/api/data/progress_chart_view/', views.RiskProgressChartView.as_view(), name='risk_progress'),
    path('risk/statistics/api/data/risk_dept_distribution/', views.RiskByDeptSummary.as_view(), name='risk_dept_summary'),
    path('risk/statistics/api/data/risk_pie_summary_by_department/', views.RiskPieSummaryByDepartment.as_view(), name='risk_pie_summary_by_department'),
    path('risk/pinned/', views.RiskPinned.as_view(), name='risk_pinned'),

    path('departments/', views.DepartmentListView.as_view(), name='dept_list'),
    path('departments/add/', views.DepartmentAddView.as_view(), name='dept_create'),
    path('departments/<int:pk>/', views.DepartmentUpdateView.as_view(), name='dept_read'),
    path('departments/<int:pk>/update/', views.DepartmentUpdateView.as_view(), name='dept_update'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='dept_delete'),

    path('staffs/', views.StaffListView.as_view(), name='staff_list'),
    path('staffs/add/', views.StaffAddView.as_view(), name='staff_create'),
    path('staffs/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff_delete'),
    path('staffs/<int:pk>/update/', views.StaffUpdateView.as_view(), name='staff_update'),
    path('staffs/<int:pk>/update/profile_pic/', views.UpdateStaffProfilePicView.as_view(), name='staff_update_pic'),
    path('staffs/<int:pk>/update/profile_image/', views.UpdateUploadedProfilePicView.as_view(), name='staff_update_image'),

    path('risk/pages/403/', views.Page403.as_view(), name='page_403'),
]
