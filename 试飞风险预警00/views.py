import json

import requests
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from datetime import datetime
from django.contrib import messages
from rest_framework.generics import ListAPIView
from django.db.models import Sum, Count

from FM.filters import FlyTaskFilter
from FM.models import *
from FM.serializers import FlyTaskSerializer
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
import logging
import numpy as np
from joblib import load

# clf_xgboost = load(r"C:\Users\n\PycharmProjects\FlyRisk00-zzb\templates\机器学习模型\model_xgboost.joblib")
clf_svm = load(r"C:\Users\n\PycharmProjects\FlyRisk00-zzb\templates\机器学习模型\model_svm.joblib")
clf_logistic = load(r"C:\Users\n\PycharmProjects\FlyRisk00-zzb\templates\机器学习模型\model_logistic.joblib")
clf_knn = load(r"C:\Users\n\PycharmProjects\FlyRisk00-zzb\templates\机器学习模型\model_knn.joblib")
clf_DecisionTree = load(r"C:\Users\n\PycharmProjects\FlyRisk00-zzb\templates\机器学习模型\model_DecisionTree.joblib")
models=[clf_knn,clf_DecisionTree,clf_logistic,clf_svm]
models_name=['knn','DecisionTree','logistic','svm']


# 重写构造JSON类
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def _login(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next = request.GET.get('next', '')
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if next == '':
                    return redirect(reverse('index'))
                else:
                    return redirect(next)
            else:
                messages.success(request, "登录失败了，请检查用户名或密码后重新登录。")
    logger = logging.getLogger('django')
    logger.error('5555')
    return render(request, 'login.html')


def _logout(request):
    logout(request)
    return redirect(reverse('index'))


@login_required()
def index(request):
    return render(request, 'index.html', {'user': request.user.username})


def index1(request):
    return render(request, 'index1.html')


def log(request):
    return render(request, 'log.html')


def scenemanagement(request):
    return render(request, '试飞风险知识库/试飞科目/scene_management.html')


def subjectmanagement(request):
    # return render(request, '试飞风险知识库/试飞科目/subject_management.html')
    subject_list_0 = SubjectHarm.objects.all().values_list('applicable_subject').distinct()
    subject_list = [x[0] for x in subject_list_0]
    for s in subject_list:
        Subject.objects.update_or_create(
            defaults={},
            name=s
        )
    return redirect('/admin/FM/subject/')


def taskmanagement(request):
    model = FlyTask
    fields = model._meta.fields
    fields_name_list = [fields[i].name for i in range(len(fields))]
    verbose_name_list = [model._meta.get_field(f).verbose_name for f in fields_name_list]
    my_table_name = model._meta.verbose_name
    my_table_name_en = model._meta.model_name
    context = {'fields_name_list': fields_name_list, 'verbose_name_list': verbose_name_list,
               'my_table_name': my_table_name, 'my_table_name_en': my_table_name_en}
    return render(request, '试飞风险预测预警/试飞任务/task_management.html', context)


class FlyTaskViewSet(ListAPIView):
    out = 0
    queryset = FlyTask.objects.all()  # 获取数据
    serializer_class = FlyTaskSerializer  # 指定序列化类
    filter_class = FlyTaskFilter  # 指定过滤器类


def taskinfo(request):
    json_data = {"code": 0, "msg": "", "count": 1000, "data": []}

    data = json.loads(requests.get('http://127.0.0.1:8000/FM/FlyTask/').text)
    page_index = request.GET.get('page')
    page_limit = request.GET.get('limit')
    p = Paginator(data, page_limit)
    json_data['data'] = p.page(page_index).object_list
    json_data['count'] = len(data)
    # print(json_data)
    return HttpResponse(json.dumps(json_data))


def taskdataadd(request):
    if request.method == "POST":
        model = FlyTask
        fields = model._meta.fields
        fields_name_list = [fields[i].name for i in range(len(fields))]
        my_dict = {}
        for f in fields_name_list:
            my_dict[f] = request.POST.get(f, '-')
        # print(my_dict)
        my_instance = model(**my_dict)
        my_instance.save()

        return HttpResponse(json.dumps("yes"))
    subjects = [x[0] for x in Subject.objects.all().values_list('name')]
    print(subjects)

    return render(request, '试飞风险预测预警/试飞任务/data_add0.html', {'subjects': subjects})


def taskdatadel(request):
    ids = json.loads(request.POST.get('id'))
    for i in ids:
        FlyTask.objects.get(id=i).delete()
    return HttpResponse(json.dumps(''))


def taskindex(request):
    id = request.GET.get('id')
    status = request.GET.get('status')
    context = {'id': id, 'status': status}
    return render(request, '试飞风险预测预警/试飞任务/task_index.html', context=context)


def risksource(request):
    return render(request, '试飞风险知识库/危险源库/risk_source.html')


def risksourceadd(request):
    return render(request, '试飞风险知识库/危险源库/risk_source_add.html')


def risksource_data(request):
    json_data = {"code": 0, "msg": "", "count": 1000, "data": []}
    # data = json.loads(requests.get('http://127.0.0.1:8000/QE/ProductionQuality/').text)
    risksource_data = RiskSource.objects.all()
    data0 = json.loads(serializers.serialize('json', risksource_data).replace("'", '"'))
    data = []
    for i in data0:
        i['fields']['id'] = i['pk']
        data.append(i['fields'])
    page = 1
    limit = 10000
    p = Paginator(data, limit)
    json_data['data'] = p.page(page).object_list
    json_data['count'] = len(data)
    # print(json_data)
    return HttpResponse(json.dumps(json_data))


def subjectharm(request):
    return render(request, '试飞风险知识库/试飞科目危害库/subject_harm.html')


def subjectharmadd(request):
    return render(request, '试飞风险知识库/试飞科目危害库/subject_harm_add.html')


def subjectharm_data(request):
    json_data = {"code": 0, "msg": "", "count": 1000, "data": []}
    # data = json.loads(requests.get('http://127.0.0.1:8000/QE/ProductionQuality/').text)
    subjectharm_data = SubjectHarm.objects.all()
    data0 = json.loads(serializers.serialize('json', subjectharm_data).replace("'", '"'))
    data = []
    for i in data0:
        i['fields']['id'] = i['pk']
        data.append(i['fields'])
    page = 1
    limit = 10000
    p = Paginator(data, limit)
    json_data['data'] = p.page(page).object_list
    json_data['count'] = len(data)
    # print(json_data)
    return HttpResponse(json.dumps(json_data))


def expertknow(request):
    return render(request, '试飞风险知识库/专家知识库/expert_know.html')


def expertknowadd(request):
    return render(request, '试飞风险知识库/专家知识库/expert_know_add.html')


def expertknowana(request):
    return render(request, '试飞风险知识库/专家知识库/expert_ana.html')


def simulation(request):
    return render(request, '试飞风险预测预警/试飞仿真推演/simulation.html')


def beforefly_select(request):
    ids = FlyTask.objects.values('id')
    my_items = [x['id'] for x in ids]
    context = {'my_items': my_items}
    # print(context)
    return render(request, '试飞风险预测预警/事前预测/select_task.html', context=context)


def duringfly_select(request):
    ids = FlyTask.objects.values('id')
    my_items = [x['id'] for x in ids]
    context = {'my_items': my_items}
    # print(context)
    return render(request, '试飞风险预测预警/实时预警/select_task.html', context=context)


def beforefly(request):
    return render(request, '试飞风险预测预警/事前预测/before_fly.html')


def duringfly(request):
    return render(request, '试飞风险预测预警/实时预警/during_fly.html')


def risk_notice(request):
    """
    风险评估表
    in: task_id
    """
    id = request.GET.get('id')
    # 取出id的试飞任务实例
    task = FlyTask.objects.filter(id=id).first()

    subject = task.subject
    subject_list = [x for x in subject.split(',')]

    # 表2，危害表
    # 先生成危害表和危险源表好点
    qs = serializers.serialize('python', SubjectHarm.objects.filter(applicable_subject__in=subject_list))
    table2 = [{'id': i + 1, 'c1': qs[i]['fields']['harm_number'], 'c2': qs[i]['fields']['harm_name'],
               'c3': qs[i]['fields']['harm_level'], 'c4': qs[i]['fields']['harm_result'],
               'c5': qs[i]['fields']['counter_measures']} for i in range(len(qs))]

    # table2 = [{'id': 1, 'c1': 'AG600-THA-043', 'c2': '投水舱门故障',
    #            'c3': '低', 'c4': '机组工作负荷增加',
    #            'c5': '1） 机务人员根据机务飞行准备卡 4 完成灭火任务系统地面自检，投水舱门收放功能正常；2） 机组经过空勤理论培训，清楚投水舱门放下时的限制飞行速度；3） 任务单中明确投水舱门放下 300km/h 限制要求；4） 地面人员监控飞机投水舱门状态和 EICAS 告警信息，若出现异常及时报告监控指挥员和机组。'},
    #           {'id': '...', 'c1': '...', 'c2': '...',
    #            'c3': '...', 'c4': '...', 'c5': '...'},
    #           ]
    # 表3，危险源表
    subjectharm_name_list = [x['c2'] for x in table2]
    risksource_name_list_0 = RiskSource_By_SubjectHarm.objects.filter(
        subjectharm_name__in=subjectharm_name_list).values_list('risksource_name').distinct()
    risksource_name_list = [x[0] for x in risksource_name_list_0]

    qs = serializers.serialize('python', RiskSource.objects.filter(risk_source__in=risksource_name_list))

    table3 = [{'id': i + 1, 'c1': qs[i]['pk'], 'c2': qs[i]['fields']['risk_source'],
               'c3': qs[i]['fields']['risk_level'], 'c4': qs[i]['fields']['risk_source_result'],
               'c5': qs[i]['fields']['counter_measures']} for i in range(len(qs))]

    # table3 = [{'id': 1, 'c1': 'SF-JC-JWWX-0022/Q', 'c2': '机上存在多余物',
    #            'c3': '中', 'c4': '多余物损伤机体，造成设备受损和系统失效。',
    #            'c5': '1. 工具、设备标识清晰；2. 制定工具防遗失、散落的工作流程，严格执行工具三清点要求；3. 工作中注意防范因工作产生的多余物；4. 工作结束后，清理复查工作部位，防止多余物遗留在机上。'},
    #           {'id': '...', 'c1': '...', 'c2': '...',
    #            'c3': '...', 'c4': '...', 'c5': '...'},
    #           ]

    # 表1，科目风险表
    table1 = []
    for i in range(len(subject_list)):
        dict_table1 = {'id': 1, 'c2': task.id, 'c1': subject_list[i]}
        dict_table1['c3'] = '、'.join([x['c2'] for x in table2])
        risk_level_list = [x['c3'] for x in table2]
        if '高' in risk_level_list:
            dict_table1['c4'] = '高'
        elif '中' in risk_level_list:
            dict_table1['c4'] = '中'
        else:
            dict_table1['c4'] = '低'
        table1.append(dict_table1)

    # table1 = [{'id': 1, 'c1': '注水投水、汲水投水演示 2', 'c2': 'SY D0230K217C1',
    #            'c3': '投水舱门故障、投水舱门载荷超限、不对称汲水、汲水斗收放不到位、飞机姿态扰动', 'c4': '低'},
    #           {'id': 2, 'c1': '投汲水飞行 3', 'c2': ' SY D0230K220C1',
    #            'c3': '投水舱门故障、投水舱门载荷超限、不对称汲水、汲水斗收放不到位、飞机姿态扰动', 'c4': '低'},
    #           {'id': 3, 'c1': '注水投水、汲水投水演示 2', 'c2': 'SY D0230K217C1',
    #            'c3': '投水舱门故障、投水舱门载荷超限、不对称汲水、汲水斗收放不到位、飞机姿态扰动', 'c4': '低'},
    #           {'id': 4, 'c1': '改装培训（宜昌陆上起落）', 'c2': 'SY D0230K224C1（主计划）',
    #            'c3': '飞机冲出跑道、飞机响应异常、飞机通信中断', 'c4': '低'},
    #           {'id': 5, 'c1': '改装培训（陆上起落及空域训练）', 'c2': 'SY D0230K225C1（备份计划）',
    #            'c3': '飞机冲出跑道、飞机响应异常、飞机通信中断', 'c4': '低'}]

    context = {'table1': table1, 'subject': subject, 'table2': table2, 'table3': table3}
    return render(request, '试飞风险预测预警/试飞任务/risk_notice.html', context=context)


def safe_ana_res(request):
    """
    安全性分析单
    in: task_id
    """
    id = request.GET.get('id')
    print(id)
    my_table = [{'c1': 'AG600-THA-060', 'c2': '飞机画面显示异常', 'c3': '低',
                 'c4': '低', 'c5': '机组工作负荷增加',
                 'c6': '1） 地面根据机务飞行准备卡4检查大气数据系统、航姿基准系统、无线电高度表、空管应答机、DME、VOR、ADF、卫星导航、指示/记录、电源系统、综合备份仪表、应急磁罗盘、气象雷达工作正常；\
      2） 地面人员监控大气数据系统、航姿基准系统、卫星导航、指示/记录、电源系统等参数和EICAS告警信息，若出现异常及时报告监控指挥员和机组。'},
                {'c1': 'AG600-THA-061', 'c2': '襟翼收放故障', 'c3': '低',
                 'c4': '低', 'c5': '着陆接地速度大、机组工作负荷增加', 'c6': '1） 机务人员按机务飞行准备卡1检查襟翼外观完好，按卡4检查襟翼系统工作正常；\
      2） 机组经过空勤培训，清楚襟翼在不同偏度17°、25°和40°时的限制速度； \
            3） 机组根据训练任务书经过襟翼收放功能失效的铁鸟台训练；\
            4） 任务单中明确襟翼使用限制速度；\
            5） 地面监控飞机速度、姿态参数和EICAS告警信息，若出现异常及时报告监控指挥员和机组，提醒机组注意刹车速度。'},
                {'c1': 'AG600-THA-062', 'c2': '舱内温度失调', 'c3': '低',
                 'c4': '低', 'c5': '机组工作负荷增加', 'c6': '1） 地面检查和维护工作，严格按机务飞行准备卡（4份）执行；2） 机组经过空勤理论培训，熟悉设备和系统非正常操作程序；3） 驾驶员试飞前要保持足够睡眠和良好的精神状态，以增强抗热疲劳的能力；\
      4） 试飞过程中，如飞行员感觉座舱环境难以适应可提前结束动作，下降高度返航；\
      5） 地面人员监控环控防火防冰系统画面状态参数和EICAS告警信息，若出现异常及时报告监控指挥员和机组。'},
                {'c1': '...', 'c2': '...', 'c3': '...',
                 'c4': '...', 'c5': '...', 'c6': '...'},
                ]
    context = {'my_table': my_table}
    return render(request, '试飞风险预测预警/事前预测/安全性分析单.html', context=context)


def risk_identify(request):
    return render(request, '试飞任务风险识别分析/risk_identify.html')


def fengxian(request):
    return render(request, '试飞任务风险识别分析/fengxian.html')


def weixianyuan_initial_detail(request):
    id = request.GET.get('id')
    data = InitialRiskSource.objects.get(id=id)
    return render(request, '试飞任务风险识别分析/initial_risk_resource_detail.html', {'data': data, 'id': id})


def weixianyuan_initial_alter(request):
    if request.method == 'POST':
        data_post = json.loads(request.body)['data']
        data_dict = {}
        for i in data_post:
            data_dict[list(i.keys())[0]] = list(i.values())[0]
        # print(data_dict)
        if data_dict['status'] == '保存':
            InitialRiskSource.objects.filter(id=data_dict['id']).update(work_stage=data_dict['liucheng'],
                                                                        plane_type=data_dict['check0'],
                                                                        department=data_dict['check1'],
                                                                        risk_source=data_dict['text3'],
                                                                        risk_source_result=data_dict['text4'],
                                                                        reason1=data_dict['yinsu1'],
                                                                        reason2=data_dict['yinsu2'],
                                                                        reason3=data_dict['yinsu3'],
                                                                        reason4=data_dict['yinsu4'],
                                                                        R_value=data_dict['R_score'],
                                                                        risk_level=data_dict['R_level'],
                                                                        counter_measures=data_dict['text5'],
                                                                        left_risk_level=data_dict['text6'],
                                                                        status=data_dict['status'],
                                                                        question_new1=data_dict['text1'],
                                                                        question_new2=data_dict['text2'],
                                                                        probability=data_dict['check2'],
                                                                        seriousness=data_dict['check3'],
                                                                        fkey=RiskSourceActivity.objects.get(
                                                                            id=data_dict['activity_id']),
                                                                        status_activity='未提交')
        elif json.loads(request.body)['role'] == '2':
            x = InitialRiskSource(work_stage=data_dict['liucheng'], plane_type=data_dict['check0'],
                                  department=data_dict['check1'], risk_source=data_dict['text3'],
                                  risk_source_result=data_dict['text4'], reason1=data_dict['yinsu1'],
                                  reason2=data_dict['yinsu2'], reason3=data_dict['yinsu3'],
                                  reason4=data_dict['yinsu4'], R_value=data_dict['R_score'],
                                  risk_level=data_dict['R_level'], counter_measures=data_dict['text5'],
                                  left_risk_level=data_dict['text6'], status=data_dict['status'],
                                  question_new1=data_dict['text1'], question_new2=data_dict['text2'],
                                  probability=data_dict['check2'], seriousness=data_dict['check3'],
                                  fkey=RiskSourceActivity.objects.get(id=data_dict['id']),
                                  creator=InitialRiskSource.objects.get(id=data_dict['id2']).creator,
                                  status_activity='审核人员已修改')
            x.save()
            InitialRiskSource.objects.filter(id=json.loads(request.body)['id']).update(
                status_activity='审核人员已修改（原问卷）')
        elif json.loads(request.body)['role'] == '3':
            x = InitialRiskSource(work_stage=data_dict['liucheng'], plane_type=data_dict['check0'],
                                  department=data_dict['check1'], risk_source=data_dict['text3'],
                                  risk_source_result=data_dict['text4'], reason1=data_dict['yinsu1'],
                                  reason2=data_dict['yinsu2'], reason3=data_dict['yinsu3'],
                                  reason4=data_dict['yinsu4'], R_value=data_dict['R_score'],
                                  risk_level=data_dict['R_level'], counter_measures=data_dict['text5'],
                                  left_risk_level=data_dict['text6'], status=data_dict['status'],
                                  question_new1=data_dict['text1'], question_new2=data_dict['text2'],
                                  probability=data_dict['check2'], seriousness=data_dict['check3'],
                                  fkey=RiskSourceActivity.objects.get(id=data_dict['id']),
                                  creator=InitialRiskSource.objects.get(id=data_dict['id2']).creator,
                                  status_activity='专家已修改')
            x.save()
            InitialRiskSource.objects.filter(id=json.loads(request.body)['id']).update(
                status_activity='专家已修改（原问卷）')
        return JsonResponse({'msg': '修改成功！'}, safe=False)

    else:
        role = request.GET.get('role')
        activity_id = request.GET.get('ac_id')
        id = request.GET.get('id')
        data = InitialRiskSource.objects.get(id=id)
        return render(request, '试飞任务风险识别分析/initial_risk_resource_alter.html',
                      {'data': data, 'id': id, 'activity_id': activity_id, 'role': role})


def weixianyuan_initial_alter_save(request):
    activity_id = request.GET.get('ac_id')
    id = request.GET.get('id')
    data = InitialRiskSource.objects.get(id=id)
    return render(request, '试飞任务风险识别分析/initial_risk_resource_alter_save.html',
                  {'data': data, 'id': id, 'activity_id': activity_id})


def weixianyuan_initial(request):
    model = InitialRiskSource
    fields = model._meta.fields
    fields_name_list = [fields[i].name for i in range(len(fields))]
    verbose_name_list = [model._meta.get_field(f).verbose_name for f in fields_name_list]
    my_table_name = model._meta.verbose_name
    my_table_name_en = model._meta.model_name
    context = {'fields_name_list': fields_name_list, 'verbose_name_list': verbose_name_list,
               'my_table_name': my_table_name, 'my_table_name_en': my_table_name_en,
               'fkey_id': request.GET.get('fkey_id'),
               'status_activity': RiskSourceActivity.objects.get(id=request.GET.get('fkey_id')).status_activity}
    context['filter_dict'] = request.GET
    return render(request, '试飞任务风险识别分析/initial_risk_resource.html', context=context)


def weixianyuan_initial_mine(request):
    model = InitialRiskSource
    fields = model._meta.fields
    fields_name_list = [fields[i].name for i in range(len(fields))]
    verbose_name_list = [model._meta.get_field(f).verbose_name for f in fields_name_list]
    my_table_name = model._meta.verbose_name
    my_table_name_en = model._meta.model_name
    context = {'fields_name_list': fields_name_list, 'verbose_name_list': verbose_name_list,
               'my_table_name': my_table_name, 'my_table_name_en': my_table_name_en,
               'fkey_id': request.GET.get('fkey_id'),
               'user': request.user.username,
               'status_activity': RiskSourceActivity.objects.get(id=request.GET.get('fkey_id')).status_activity}
    context['filter_dict'] = request.GET
    return render(request, '试飞任务风险识别分析/initial_risk_resource_mine.html', context=context)


def weixianyuan_activity(request):
    model = RiskSourceActivity
    fields = model._meta.fields
    fields_name_list = [fields[i].name for i in range(len(fields))]
    verbose_name_list = [model._meta.get_field(f).verbose_name for f in fields_name_list]
    my_table_name = model._meta.verbose_name
    my_table_name_en = model._meta.model_name
    user = request.user.username
    group_list = []
    if request.user.groups.filter(name='审核人员').exists():
        group_list.append('审核人员')
    if request.user.groups.filter(name='部门人员').exists():
        group_list.append('部门人员')
    # print(group_list)
    context = {'fields_name_list': fields_name_list, 'verbose_name_list': verbose_name_list,
               'my_table_name': my_table_name, 'my_table_name_en': my_table_name_en, 'user': user,
               'group_list': group_list}
    return render(request, '试飞任务风险识别分析/weixianyuan_activity.html', context=context)


def weixianyuan(request):
    return render(request, '试飞任务风险识别分析/weixianyuan.html')


def weixianyuan_initial_add(request):
    if request.method == 'POST':
        data_post = json.loads(request.body)['data']
        data_dict = {}
        for i in data_post:
            data_dict[list(i.keys())[0]] = list(i.values())[0]
        x = InitialRiskSource(work_stage=data_dict['liucheng'], plane_type=data_dict['check0'],
                              department=data_dict['check1'], risk_source=data_dict['text3'],
                              risk_source_result=data_dict['text4'], reason1=data_dict['yinsu1'],
                              reason2=data_dict['yinsu2'], reason3=data_dict['yinsu3'], reason4=data_dict['yinsu4'],
                              R_value=data_dict['R_score'], risk_level=data_dict['R_level'],
                              counter_measures=data_dict['text5'], left_risk_level=data_dict['text6'],
                              status=data_dict['status'], status_activity=data_dict['status_activity'],
                              question_new1=data_dict['text1'], question_new2=data_dict['text2'],
                              probability=data_dict['check2'], seriousness=data_dict['check3'],
                              fkey=RiskSourceActivity.objects.get(id=data_dict['id']),
                              creator=request.user.username)
        x.save()
        return JsonResponse({'msg': '添加成功！'}, safe=False)
    if request.method == 'GET':
        return render(request, '试飞任务风险识别分析/initial_risk_resource_add.html',
                      {'liucheng': "飞行", 'id': request.GET['id']})


def weixianyuan_add_ku(request):
    ids = json.loads(request.POST.get('ids'))
    # InitialRiskSource.objects.filter(fkey=request.POST.get('fkey_id')).update(status_activity='等待审核')
    if ids == 2:
        RiskSourceActivity.objects.filter(id=request.POST.get('fkey_id')).update(status_activity='专家评审中')
        InitialRiskSource.objects.filter(fkey=request.POST.get('fkey_id'),
                                         status_activity__in=['审核通过', '审核人员已修改']).update(
            status_activity='等待专家评审')
    elif InitialRiskSource.objects.get(id=ids[0]).status_activity == '等待审核':
        InitialRiskSource.objects.filter(fkey=request.POST.get('fkey_id'), status_activity='等待审核').update(
            status_activity='审核未通过')
        for i in ids:
            InitialRiskSource.objects.filter(id=i).update(status_activity='审核通过')
        RiskSourceActivity.objects.filter(id=request.POST.get('fkey_id')).update(status_activity='部门审核中')
    elif InitialRiskSource.objects.get(id=ids[0]).status_activity in ['等待专家评审', '专家已修改']:
        InitialRiskSource.objects.filter(fkey=request.POST.get('fkey_id'),
                                         status_activity__in=['等待专家评审', '专家已修改']).update(
            status_activity='专家评审未通过')
        for i in ids:
            a = InitialRiskSource.objects.get(id=i)
            x = RiskSource(work_stage=a.work_stage, plane_type=a.plane_type, subject='',
                           risk_source=a.risk_source,
                           risk_source_result=a.risk_source_result, R_value=a.R_value, risk_level=a.risk_level,
                           counter_measures=a.counter_measures,
                           derive_R_value='', derive_counter_measures='', left_risk_level=a.left_risk_level,
                           approver='', counter_measures_result='', remarks='')
            x.save()
            InitialRiskSource.objects.filter(id=i).update(status_activity='已进入危险源库')
        RiskSourceActivity.objects.filter(id=request.POST.get('fkey_id')).update(status_activity='活动结束')

    return HttpResponse(json.dumps('123'))


def weihai_initial_detail(request):
    id = request.GET.get('id')
    data = InitialSubjectHarm.objects.get(id=id)
    return render(request, '试飞任务风险识别分析/initial_weihai_detail.html', {'data': data, 'id': id})


def weihai_initial_alter(request):
    if request.method == 'POST':
        data_post = json.loads(request.body)['data']
        data_dict = {}
        for i in data_post:
            data_dict[list(i.keys())[0]] = list(i.values())[0]
        # print(data_dict)
        if data_dict['status'] == '保存':
            InitialSubjectHarm.objects.filter(id=data_dict['id']).update(subject=data_dict['subject'],
                                                                         plane_type=data_dict['check0'],
                                                                         harm_name=data_dict['text1'],
                                                                         probability=data_dict['check2'],
                                                                         seriousness=data_dict['check3'],
                                                                         R_value=data_dict['R_value'],
                                                                         harm_result=data_dict['text2'],
                                                                         harm_level=data_dict['harm_level'],
                                                                         subject_type=data_dict['check4'],
                                                                         measure1=data_dict['text3'],
                                                                         measure2=data_dict['text4'],
                                                                         left_harm_score=data_dict['text5'],
                                                                         left_harm_level=data_dict['text6'],
                                                                         status=data_dict['status'],
                                                                         fkey=SubjectHarmActivity.objects.get(
                                                                             id=data_dict['activity_id']),
                                                                         status_activity='未提交')
        elif json.loads(request.body)['role'] == '2':
            x = InitialSubjectHarm(subject=data_dict['subject'], plane_type=data_dict['check0'],
                                   harm_name=data_dict['text1'], probability=data_dict['check2'],
                                   seriousness=data_dict['check3'], R_value=data_dict['R_value'],
                                   harm_result=data_dict['text2'], harm_level=data_dict['harm_level'],
                                   subject_type=data_dict['check4'],
                                   measure1=data_dict['text3'], measure2=data_dict['text4'],
                                   left_harm_score=data_dict['text5'], left_harm_level=data_dict['text6'],
                                   status=data_dict['status'], fkey=SubjectHarmActivity.objects.get(id=data_dict['id']),
                                   creator=InitialRiskSource.objects.get(id=data_dict['id2']).creator,
                                   status_activity='审核人员已修改')
            x.save()
            InitialSubjectHarm.objects.filter(id=json.loads(request.body)['id']).update(
                status_activity='审核人员已修改（原问卷）')
        elif json.loads(request.body)['role'] == '3':
            x = InitialSubjectHarm(subject=data_dict['subject'], plane_type=data_dict['check0'],
                                   harm_name=data_dict['text1'], probability=data_dict['check2'],
                                   seriousness=data_dict['check3'], R_value=data_dict['R_value'],
                                   harm_result=data_dict['text2'], harm_level=data_dict['harm_level'],
                                   subject_type=data_dict['check4'],
                                   measure1=data_dict['text3'], measure2=data_dict['text4'],
                                   left_harm_score=data_dict['text5'], left_harm_level=data_dict['text6'],
                                   status=data_dict['status'], fkey=SubjectHarmActivity.objects.get(id=data_dict['id']),
                                   creator=InitialRiskSource.objects.get(id=data_dict['id2']).creator,
                                   status_activity='专家已修改')
            x.save()
            InitialSubjectHarm.objects.filter(id=json.loads(request.body)['id']).update(
                status_activity='专家已修改（原问卷）')
        return JsonResponse({'msg': '修改成功！'}, safe=False)

    else:
        role = request.GET.get('role')
        activity_id = request.GET.get('ac_id')
        id = request.GET.get('id')
        data = InitialSubjectHarm.objects.get(id=id)
        return render(request, '试飞任务风险识别分析/initial_weihai_alter.html',
                      {'data': data, 'id': id, 'activity_id': activity_id, 'role': role})


def weihai_initial_alter_save(request):
    activity_id = request.GET.get('ac_id')
    id = request.GET.get('id')
    data = InitialSubjectHarm.objects.get(id=id)
    return render(request, '试飞任务风险识别分析/initial_weihai_alter_save.html',
                  {'data': data, 'id': id, 'activity_id': activity_id})


def weihai_initial(request):
    model = InitialSubjectHarm
    fields = model._meta.fields
    fields_name_list = [fields[i].name for i in range(len(fields))]
    verbose_name_list = [model._meta.get_field(f).verbose_name for f in fields_name_list]
    my_table_name = model._meta.verbose_name
    my_table_name_en = model._meta.model_name
    context = {'fields_name_list': fields_name_list, 'verbose_name_list': verbose_name_list,
               'my_table_name': my_table_name, 'my_table_name_en': my_table_name_en,
               'fkey_id': request.GET.get('fkey_id'),
               'status_activity': SubjectHarmActivity.objects.get(id=request.GET.get('fkey_id')).status_activity}
    context['filter_dict'] = request.GET
    return render(request, '试飞任务风险识别分析/initial_weihai.html', context=context)


def weihai_initial_mine(request):
    model = InitialSubjectHarm
    fields = model._meta.fields
    fields_name_list = [fields[i].name for i in range(len(fields))]
    verbose_name_list = [model._meta.get_field(f).verbose_name for f in fields_name_list]
    my_table_name = model._meta.verbose_name
    my_table_name_en = model._meta.model_name
    context = {'fields_name_list': fields_name_list, 'verbose_name_list': verbose_name_list,
               'my_table_name': my_table_name, 'my_table_name_en': my_table_name_en,
               'fkey_id': request.GET.get('fkey_id'),
               'user': request.user.username,
               'status_activity': SubjectHarmActivity.objects.get(id=request.GET.get('fkey_id')).status_activity}
    context['filter_dict'] = request.GET
    return render(request, '试飞任务风险识别分析/initial_weihai_mine.html', context=context)


def weihai_activity(request):
    model = SubjectHarmActivity
    fields = model._meta.fields
    fields_name_list = [fields[i].name for i in range(len(fields))]
    verbose_name_list = [model._meta.get_field(f).verbose_name for f in fields_name_list]
    my_table_name = model._meta.verbose_name
    my_table_name_en = model._meta.model_name
    user = request.user.username
    group_list = []
    if request.user.groups.filter(name='审核人员').exists():
        group_list.append('审核人员')
    if request.user.groups.filter(name='部门人员').exists():
        group_list.append('部门人员')
    # print(group_list)
    context = {'fields_name_list': fields_name_list, 'verbose_name_list': verbose_name_list,
               'my_table_name': my_table_name, 'my_table_name_en': my_table_name_en, 'user': user,
               'group_list': group_list}
    return render(request, '试飞任务风险识别分析/weihai_activity.html', context=context)


def weihai(request):
    return render(request, '试飞任务风险识别分析/weihai.html')


def weihai_initial_add(request):
    if request.method == 'POST':
        data_post = json.loads(request.body)['data']
        data_dict = {}
        for i in data_post:
            data_dict[list(i.keys())[0]] = list(i.values())[0]
        if 'del_id' in list(data_dict.keys()):
            InitialSubjectHarm.objects.filter(id=data_dict['del_id']).delete()
        x = InitialSubjectHarm(subject=data_dict['subject'], plane_type=data_dict['check0'],
                               harm_name=data_dict['text1'], probability=data_dict['check2'],
                               seriousness=data_dict['check3'], R_value=data_dict['R_value'],
                               harm_result=data_dict['text2'], harm_level=data_dict['harm_level'],
                               subject_type=data_dict['check4'],
                               measure1=data_dict['text3'], measure2=data_dict['text4'],
                               left_harm_score=data_dict['text5'], left_harm_level=data_dict['text6'],
                               status=data_dict['status'], fkey=SubjectHarmActivity.objects.get(id=data_dict['id']),
                               status_activity=data_dict['status_activity'],
                               creator=request.user.username)
        x.save()
        return JsonResponse({'msg': '添加成功！'}, safe=False)
    if request.method == 'GET':
        return render(request, '试飞任务风险识别分析/initial_weihai_add.html',
                      {'subject': "飞行", 'id': request.GET['id']})


def weihai_add_ku(request):
    ids = json.loads(request.POST.get('ids'))
    # InitialRiskSource.objects.filter(fkey=request.POST.get('fkey_id')).update(status_activity='等待审核')
    if ids == 2:
        SubjectHarmActivity.objects.filter(id=request.POST.get('fkey_id')).update(status_activity='专家评审中')
        InitialSubjectHarm.objects.filter(fkey=request.POST.get('fkey_id'),
                                          status_activity__in=['审核通过', '审核人员已修改']).update(
            status_activity='等待专家评审')
    elif InitialSubjectHarm.objects.get(id=ids[0]).status_activity == '等待审核':
        InitialSubjectHarm.objects.filter(fkey=request.POST.get('fkey_id'), status_activity='等待审核').update(
            status_activity='审核未通过')
        for i in ids:
            InitialSubjectHarm.objects.filter(id=i).update(status_activity='审核通过')
        SubjectHarmActivity.objects.filter(id=request.POST.get('fkey_id')).update(status_activity='部门审核中')
    elif InitialSubjectHarm.objects.get(id=ids[0]).status_activity in ['等待专家评审', '专家已修改']:
        InitialSubjectHarm.objects.filter(fkey=request.POST.get('fkey_id'),
                                          status_activity__in=['等待专家评审', '专家已修改']).update(
            status_activity='专家评审未通过')
        for i in ids:
            a = InitialSubjectHarm.objects.get(id=i)
            x = SubjectHarm(plane_type=a.plane_type, harm_name=a.harm_name, R_value=a.R_value,
                            harm_level=a.harm_level, subject_type=a.subject_type, harm_result=a.harm_result,
                            counter_measures=a.measure1, emergency_response_measures=a.measure2,
                            left_R_value=a.left_harm_score,
                            left_harm_level=a.left_harm_level, remarks='')
            x.save()
            InitialSubjectHarm.objects.filter(id=i).update(status_activity='已进入危险源库')
        SubjectHarmActivity.objects.filter(id=request.POST.get('fkey_id')).update(status_activity='活动结束')

    return HttpResponse(json.dumps('123'))


# def weihai_initial(request):
#     id = request.GET.get('id')
#     model = InitialSubjectHarm
#     fields = model._meta.fields
#     fields_name_list = [fields[i].name for i in range(len(fields))]
#     verbose_name_list = [model._meta.get_field(f).verbose_name for f in fields_name_list]
#     my_table_name = model._meta.verbose_name
#     my_table_name_en = model._meta.model_name
#     context = {'fields_name_list': fields_name_list, 'verbose_name_list': verbose_name_list,'user':request.user.username,
#                'my_table_name': my_table_name, 'my_table_name_en': my_table_name_en, 'id': id}
#     return render(request, '试飞任务风险识别分析/initial_weihai.html', context=context)
# def weihai_activity(request):
#     model = SubjectHarmActivity
#     fields = model._meta.fields
#     fields_name_list = [fields[i].name for i in range(len(fields))]
#     verbose_name_list = [model._meta.get_field(f).verbose_name for f in fields_name_list]
#     my_table_name = model._meta.verbose_name
#     my_table_name_en = model._meta.model_name
#     group_list = []
#     if request.user.groups.filter(name='审核人员').exists():
#         group_list.append('审核人员')
#     if request.user.groups.filter(name='部门人员').exists():
#         group_list.append('部门人员')
#     context = {'fields_name_list': fields_name_list, 'verbose_name_list': verbose_name_list,
#                'my_table_name': my_table_name, 'my_table_name_en': my_table_name_en,
#                'group_list':group_list, 'user':request.user.username,}
#     return render(request, '试飞任务风险识别分析/weihai_activity.html', context=context)
# def weihai(request):
#     return render(request, '试飞任务风险识别分析/weixianyuan.html')
# def weihai_initial_add(request):
#     if request.method == 'POST':
#         data_post = json.loads(request.body)['data']
#         data_dict = {}
#         for i in data_post:
#             data_dict[list(i.keys())[0]] = list(i.values())[0]
#
#         x = InitialSubjectHarm(subject=data_dict['subject'], plane_type=data_dict['check0'],
#                                harm_name=data_dict['text1'], probability=data_dict['check2'],
#                                seriousness=data_dict['check3'], risk_level=data_dict['R_level'],
#                                reason=str(data_dict['getData']), harm_result=data_dict['text2'],
#                                subject_type=data_dict['check4'],
#                                measure1=data_dict['text3'], measure2=data_dict['text4'],
#
#                                left_harm_score=data_dict['text5'], left_harm_level=data_dict['text6'],
#                                status=data_dict['status'])
#         x.save()
#         return JsonResponse({'msg': '添加成功！'}, safe=False)
#     if request.method == 'GET':
#         return render(request, '试飞任务风险识别分析/initial_weihai_add.html',
#                       {'subject': "飞行", 'id': request.GET['id']})
#

def weixianyuan_by_weihai(request):
    if request.method == 'GET':
        model = RiskSource_By_SubjectHarm
        fields = model._meta.fields
        fields_name_list = [fields[i].name for i in range(len(fields))]
        verbose_name_list = [model._meta.get_field(f).verbose_name for f in fields_name_list]
        my_table_name = model._meta.verbose_name
        my_table_name_en = model._meta.model_name
        context = {'fields_name_list': fields_name_list, 'verbose_name_list': verbose_name_list,
                   'my_table_name': my_table_name, 'my_table_name_en': my_table_name_en}
        return render(request, '试飞任务风险识别分析/weixianyuan_by_weihai.html', context=context)


def weixianyuan_by_weihai_add(request):
    if request.method == 'POST':
        data_post = json.loads(request.body)['data']
        data_dict = {}
        for i in data_post:
            data_dict[list(i.keys())[0]] = list(i.values())[0]
        # print(data_dict)
        x = RiskSource_By_SubjectHarm(risksource=RiskSource.objects.get(id=data_dict['check1_id']),
                                      risksource_name=data_dict['check1'],
                                      subjectharm=SubjectHarm.objects.get(id=data_dict['check2_id']),
                                      subjectharm_name=data_dict['check2'],
                                      remarks=data_dict['text1'])
        x.save()
        return JsonResponse({'msg': '添加成功！'}, safe=False)
    if request.method == 'GET':
        weixianyuan = RiskSource.objects.all()
        weihai = SubjectHarm.objects.all()
        return render(request, '试飞任务风险识别分析/weixianyuan_by_weihai_add.html',
                      {'weixianyuan': weixianyuan, 'weihai': weihai})


def check(request):
    return render(request, '试飞任务风险识别分析/check.html', {'id': 1})


# 做图表联动可视化，饼图+折线图
def flytask_ana(request):
    id_str = request.GET.get('ids')
    id_list = id_str.strip('*').split('*')
    model = FlyTask
    fields = model._meta.fields
    fields_name_list = [fields[i].name for i in range(len(fields))]

    dic_pie_items = {}
    for f in fields_name_list:
        dic_pie_items[f] = model._meta.get_field(f).verbose_name

    outdatas = {}
    for ii in dic_pie_items.keys():
        outdata0 = model.objects.filter(id__in=id_list).values(ii).annotate(number0=Count(ii))
        # 去掉None的名字
        outdata00 = []
        for one in outdata0:
            if one[ii] is None:
                pass
            else:
                outdata00.append({'value': one['number0'], 'name': one[ii]})
        outdata = sorted(outdata00, key=lambda x: x['name'])
        outdatas[dic_pie_items[ii]] = outdata
    context = {'outdatas': json.dumps(outdatas, cls=ComplexEncoder), 'pie_items': list(dic_pie_items.values())}

    return render(request, '试飞风险预测预警/试飞任务/flytask_ana.html', context)


def safe_ana(request):
    if request.method == "GET":
        id = request.GET.get('id', default='110')
        # print(id)
        tasks = FlyTask.objects.all()
        data0 = json.loads(serializers.serialize('json', tasks).replace("'", '"'))
        data = []
        for i in data0:
            if id == i['pk']:
                data.append(i)
        # print(data0)
        Scen_par_id = data[0]['fields']['subject']  # 取得对应的环境id
        if Scen_par_id == '2':
            return render(request, "试飞风险预测预警/试飞任务/data_add.html")
        else:
            return render(request, "试飞风险预测预警/试飞任务/data_add1.html")




def render_data(request):
    # print(request.user.username)
    dict_to_model = {'risksourceactivity': RiskSourceActivity, 'risksource': RiskSource, 'subjectharm': SubjectHarm,'expertkonw':ExpertKnow,
                     'initialrisksource': InitialRiskSource, 'subjectharmactivity': SubjectHarmActivity,
                     'flytask': FlyTask, 'initialsubjectharm': InitialSubjectHarm,
                     'risksource_by_subjectharm': RiskSource_By_SubjectHarm}

    model = dict_to_model[request.GET.get('my_table_name_en')]
    json_data = {"code": 0, "msg": "", "count": 1000, "data": []}

    # 是否开启筛选模式
    model_data = model.objects.all()
    dict_get = request.GET
    if len(dict_get.keys()) > 3:  # 代表传了筛选的字段
        not_keys = ['my_table_name_en', 'page', 'limit']
        for key in dict_get:
            if key not in not_keys:
                model_data = model_data.filter(**{key: eval(dict_get[key])})
    data0 = json.loads(serializers.serialize('json', model_data).replace("'", '"'))
    data = []
    for i in data0:
        i['fields']['id'] = i['pk']
        data.append(i['fields'])
    page = 1
    limit = 10000
    p = Paginator(data, limit)
    json_data['data'] = p.page(page).object_list
    json_data['count'] = len(data)
    return HttpResponse(json.dumps(json_data))


def my_data_add(request):
    dict_to_model = {'risksourceactivity': RiskSourceActivity, 'risksource': RiskSource, 'subjectharm': SubjectHarm,
                     'initialrisksource': InitialRiskSource, 'subjectharmactivity': SubjectHarmActivity,'expertkonw':ExpertKnow,
                     'flytask': FlyTask, 'initialsubjectharm': InitialSubjectHarm,
                     'risksource_by_subjectharm': RiskSource_By_SubjectHarm}
    if request.method == "POST":
        model = dict_to_model[request.POST.get('my_table_name_en')]
        fields = model._meta.fields
        fields_name_list = [fields[i].name for i in range(len(fields))]
        my_dict = {}
        for f in fields_name_list:
            my_dict[f] = request.POST.get(f, '-')
        # print(my_dict)
        my_instance = model(**my_dict)
        my_instance.save()
        return HttpResponse(json.dumps("yes"))

    model = dict_to_model[request.GET.get('my_table_name_en', )]
    fields = model._meta.fields
    fields_name_list = [fields[i].name for i in range(len(fields))]
    verbose_name_list = [model._meta.get_field(f).verbose_name for f in fields_name_list]
    fields_name_dict = {}
    for i in range(len(fields_name_list)):
        fields_name_dict[verbose_name_list[i]] = fields_name_list[i]
    context = {'fields_name_dict': fields_name_dict,
               'my_table_name_en': request.GET.get('my_table_name_en')}
    return render(request, 'my_data_add.html', context=context)


def my_data_del(request):
    dict_to_model = {'risksourceactivity': RiskSourceActivity, 'risksource': RiskSource, 'subjectharm': SubjectHarm,
                     'initialrisksource': InitialRiskSource, 'subjectharmactivity': SubjectHarmActivity,
                     'flytask': FlyTask, 'initialsubjectharm': InitialSubjectHarm,
                     'risksource_by_subjectharm': RiskSource_By_SubjectHarm}

    ids = json.loads(request.POST.get('ids'))
    model = dict_to_model[request.POST.get('my_table_name_en')]
    for i in ids:
        model.objects.get(id=i).delete()
    return HttpResponse(json.dumps(''))


def my_data_alter(request):
    dict_to_model = {'risksourceactivity': RiskSourceActivity, 'risksource': RiskSource,
                     'initialrisksource': InitialRiskSource, 'subjectharmactivity': SubjectHarmActivity,
                     'flytask': FlyTask}
    if request.method == "POST":
        model = dict_to_model[request.POST.get('my_table_name_en')]
        fields = model._meta.fields
        fields_name_list = [fields[i].name for i in range(len(fields))]
        my_dict = {}
        for f in fields_name_list:
            my_dict[f] = request.POST.get(f, '-')
        # print(my_dict)
        my_instance = model.objects.filter(id=request.POST.get('id'))
        my_instance.update(**my_dict)
        return HttpResponse(json.dumps("yes"))

    model = dict_to_model[request.GET.get('my_table_name_en')]
    id = request.GET.get('id', -1)
    fields = model._meta.fields
    fields_name_list = [fields[i].name for i in range(len(fields))]
    verbose_name_list = [model._meta.get_field(f).verbose_name for f in fields_name_list]
    fields_name_value_dict = {}
    instance_dict = model.objects.get(id=id).__dict__
    instance_dict.pop('_state')
    for i in range(len(fields_name_list)):
        fields_name_value_dict[verbose_name_list[i]] = [fields_name_list[i], instance_dict[fields_name_list[i]]]

    context = {'fields_name_value_dict': fields_name_value_dict,
               'my_table_name_en': request.GET.get('my_table_name_en'),
               'instance_dict': instance_dict}
    return render(request, 'my_data_alter.html', context=context)


#输入一系列参数，并使用知识库判断
def risk_decide(try_data_all):

    l = list(try_data_all.items())
    try_data= dict(l[:6])#取前6列结果作为知识库判断准则
    try_model=dict(l[6:])#取后几列作为机器学习
    arr = np.array(list(try_model.values())).reshape(1,5)
    # print(arr)
    # try_data = {'阶段': '汲水阶段', '舱门开关': '1', 'EICAS告警': '1', '液压压力': '83', '能见度': '4', '飞行速度': '525'}
    num2conclution={0:'低',1:'中',2:'高'}
    expertknows = ExpertKnow.objects.all()
    harms=SubjectHarm.objects.all()

    data0 = json.loads(serializers.serialize('json', expertknows).replace("'", '"'))
    data1 = json.loads(serializers.serialize('json', harms).replace("'", '"'))

    harm_data={}#存储,危害id:{危害名，措施}
    for item in data1:
        if item['fields']['harm_number'] not in harm_data.keys():
            harm_data[item['fields']['harm_number']]={'harm_name':item['fields']['harm_name'],'counter_measures':item['fields']['counter_measures']}


    data = {}
    for item in data0:#按阶段区分知识，值为列表，列表为字典，主键为参数
        if item['fields']['stage'] not in data.keys():
            stage=item['fields']['stage']
            data[stage]=[]
            for_decide={item['fields']['para_name']:[item['fields']['condition'],item['fields']['reference_val'],item['fields']['conclusion']],'危害编号':item['fields']['harm_id'],'规则编号':item['fields']['rule_dis']}#用于判断的，{参数名：[条件，参考值，结果]}
            data[stage].append(for_decide)
        else:
            stage = item['fields']['stage']
            for_decide = {item['fields']['para_name']: [item['fields']['condition'], item['fields']['reference_val'],
                                                        item['fields']['conclusion']],'危害编号':item['fields']['harm_id'],'规则描述':item['fields']['rule_dis']}  # 用于判断的，{参数名：[条件，参考值，危害编号，

            data[stage].append(for_decide)

    res_know=[]
    res_harm_id_dis=[]
    res_model=[]

    stage=try_data['阶段']
    try_data_keys=try_data.keys()
    conditions=data[stage]
    #知识库判断风险
    for item in conditions:
        if list(item.keys())[0] in try_data_keys:
            key=list(item.keys())[0]
            value=item[key]
            res_know.append(get_ice(try_data[key],value[0],value[1],value[2]))
            res_harm_id_dis.append([item[list(item.keys())[1]],item[list(item.keys())[2]]])
    print(res_know,res_harm_id_dis)
    #机器学习模型判断结果
    for model in models:
        res_model.append(model.predict(arr)[0])
        # print(res_model)


    if max(res_model)>max(res_know):
        try_data_all['危害等级']=num2conclution[max(res_model)]
        try_data_all['判断方式']=models_name[res_model.index(max(res_model))]
        try_data_all['危害']='/'
        try_data_all['缓解措施']='/'

        # print(try_data_all['判断方式'])
    else:
        try_data_all['危害等级'] = num2conclution[max(res_know)]
        id_dis=res_harm_id_dis[res_know.index(max(res_know))]#最高风险危害id和规则描述
        harm_id=id_dis[0]
        dis=id_dis[1]
        try_data_all['判断方式'] = dis
        try_data_all['危害'] = harm_data[harm_id]['harm_name']
        try_data_all['缓解措施'] = harm_data[harm_id]['counter_measures']
    now = datetime.now()
    try_data_all['时间']=now.strftime("%H:%M:%S")
    return try_data_all

#输入的参数真值，对比条件，参考值 ，结论
def get_ice(ver_num,condition,reference_val,conclusion):
    conclusion2num={'低':0,'中':1,"高":2}

    if condition=='=':
        if ver_num==reference_val:
            return conclusion2num[conclusion]
        else:
            return 0
    elif condition=='>':
        if ver_num > reference_val:
            return conclusion2num[conclusion]
        else:
            return 0
    elif condition=='<':
        if ver_num<reference_val:
            return conclusion2num[conclusion]
        else:
            return 0

#基于随机森林的风险判断





def try_an(request):
    return render(request,"试飞风险预测预警/实时预警/try.html")

json_data = {"code": 0, "msg": "", "count": 1000, "data": [],"data_name":"飞行速度"}
def process_column(request,value="飞行速度"):
    if request.method == "POST":
        csv_file = request.body
        data=json_data['data']
        # print(data)
        # print(json.loads(csv_file.decode('utf-8')))
        data.append(risk_decide(json.loads(csv_file.decode('utf-8'))))
        # 处理CSV文件
        page = 1
        limit = 10000
        p = Paginator(data, limit)
        json_data['data'] = p.page(page).object_list
        json_data['count'] = len(data)
        json_data['data_name'] = value
    #     print("POST",json_data['count'])
    # print("json_data",json_data)
    return HttpResponse(json.dumps(json_data))

def getData(request):
    if request.method == "POST":
        value = request.body
        print(value)
        # do something with value
    return render(request, "试飞风险预测预警/试飞任务/data_add1.html")
