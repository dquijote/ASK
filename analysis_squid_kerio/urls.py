from django.urls import path
from . import views

app_name = 'analysis_squid_kerio'

urlpatterns = [

    path('', views.index, name='index'),
    path('report', views.report_withoutuser, name='report_withoutuser'),
    path('report/upload', views.report_uploadLog, name='report_uploadLog'),
    path('report/user', views.report, name='report'),
    path('report/filter', views.report_filter, name='report_filter'),
    path('report/filter/user', views.report_filterDateUserSquid, name='report_filterSquidDateUser'),
    path('report/filter/date', views.reportFilterSquidDate, name='report_filter_date'),
    path('report/filter/kerio', views.report_filter_kerio, name='report_filter_kerio'),
    path('user/profile', views.user_profile, name='user_profile'),
    path('user/list', views.list_user, name='list_user'),

]