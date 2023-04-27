"""试飞风险预警00 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('0/', views.index1),
    path('logout/', views._logout),
    path('accounts/login/', views._login),
    path('log/', views.log),

    path('database/scenemanagement/', views.scenemanagement),
    path('database/subjectmanagement/', views.subjectmanagement),
    path('database/risksource/', views.risksource),
    path('database/risksourceadd/', views.risksourceadd),
    path('database/risksource/data/', views.risksource_data),
    path('database/subjectharm/', views.subjectharm),
    path('database/subjectharmadd/', views.subjectharmadd),
    path('database/subjectharm/data/', views.subjectharm_data),
    path('database/expertknow/', views.expertknow),
    path('database/expertknowadd/', views.expertknowadd),
    path('database/expertknowana/', views.expertknowana),

    path('task_index/risk_identify/', views.risk_identify),

    path('beforefly/select_task/', views.beforefly_select),
    path('task_index/predict/beforefly/', views.beforefly),
    path('duringfly/select_task/', views.duringfly_select),
    path('task_index/predict/duringfly/', views.duringfly),
    path('predict/simulation/', views.simulation),

    path('risk_notice/', views.risk_notice),

    path('safe_ana_res/', views.safe_ana_res),

    path('task_management/', views.taskmanagement),
    path('task_management/data/', views.render_data),
    path('task_management/data_add/', views.taskdataadd),
    path('task_management/data_del/', views.taskdatadel),
    path('task_management/alter/', views.my_data_alter),
    path('task_info/', views.taskinfo),
    path('FM/FlyTask/', views.FlyTaskViewSet.as_view()),
    path('task_index/', views.taskindex),
    path('task_ana/', views.flytask_ana),
    path('safe_ana/', views.safe_ana),

    path('fengxian/', views.fengxian),

    path('weixianyuan_activity/', views.weixianyuan_activity),
    path('weixianyuan_activity/data/', views.render_data),
    path('weixianyuan_activity/add/', views.my_data_add),
    path('weixianyuan_activity/data_del/', views.my_data_del),
    path('weixianyuan_activity/alter/', views.my_data_alter),
    path('weixianyuan_initial/', views.weixianyuan_initial),
    path('weixianyuan_initial/mine/', views.weixianyuan_initial_mine),
    path('weixianyuan_initial/detail/', views.weixianyuan_initial_detail),
    path('weixianyuan_initial/add/', views.weixianyuan_initial_add),
    path('weixianyuan_initial/alter/', views.weixianyuan_initial_alter),
    path('weixianyuan_initial/alter_save/', views.weixianyuan_initial_alter_save),
    path('weixianyuan_initial/data/', views.render_data),
    path('weixianyuan_initial/data_del/', views.my_data_del),
    path('weixianyuan_initial/data_add_ku/', views.weixianyuan_add_ku),

    path('weihai_activity/', views.weihai_activity),
    path('weihai_activity/data/', views.render_data),
    path('weihai_activity/add/', views.my_data_add),
    path('weihai_activity/data_del/', views.my_data_del),
    path('weihai_activity/alter/', views.my_data_alter),
    path('weihai_initial/', views.weihai_initial),
    path('weihai_initial/mine/', views.weihai_initial_mine),
    path('weihai_initial/detail/', views.weihai_initial_detail),
    path('weihai_initial/add/', views.weihai_initial_add),
    path('weihai_initial/alter/', views.weihai_initial_alter),
    path('weihai_initial/alter_save/', views.weihai_initial_alter_save),
    path('weihai_initial/data/', views.render_data),
    path('weihai_initial/data_del/', views.my_data_del),
    path('weihai_initial/data_add_ku/', views.weihai_add_ku),

    path('weixianyuan_by_weihai/', views.weixianyuan_by_weihai),  # 危险源/危害对应关系
    path('weixianyuan_by_weihai/data/', views.render_data),
    path('weixianyuan_by_weihai/add/', views.weixianyuan_by_weihai_add),
    path('weixianyuan_by_weihai/data_del/', views.my_data_del),

    path('weixianyuan/', views.weixianyuan),
    # path('weixianyuan/add/', views.weixianyuan_add),
    path('weihai/', views.weihai),
    # path('weihai/add/', views.weihai_add),
    path('check/', views.check),
    path('process-column/',views.process_column),
    path('getdata/',views.getData),

    path('ridi/',views.risk_decide),


]
