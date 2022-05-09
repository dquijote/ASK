from django.urls import path
from . import views

app_name = 'analysis_squid_kerio'

urlpatterns = [

    path('', views.index, name='index'),
    path('report', views.report_withoutuser, name='report_withoutuser'),
    path('report/user', views.report, name='report'),
    path('report/filter', views.report_filter, name='report_filter'),
    path('report/filter/kerio', views.report_filter_kerio, name='report_filter_kerio'),

]