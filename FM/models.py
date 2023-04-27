from django.db import models


# 试飞任务库
class FlyTask(models.Model):
    id = models.CharField(max_length=20, primary_key=True, verbose_name="编号")
    tabll = models.CharField(max_length=20, null=True, verbose_name="机型")
    machine_number = models.CharField(max_length=20, null=True, verbose_name="机号")
    # edit_time = models.CharField(max_length=20, null=True, verbose_name="编制日期")
    subject = models.CharField(max_length=1000, null=True, verbose_name="试飞科目")
    # distribute_time = models.DateTimeField(null=True, verbose_name="分发日期")
    # scenario = models.ForeignKey('Scenario', on_delete=models.CASCADE, verbose_name='场景编号',null=True)
    scenario = models.CharField(max_length=1000, null=True, verbose_name="场景")
    exe_status = models.CharField(max_length=20, null=True, verbose_name="执行状态",choices=[('预先准备', '预先准备'), ('直接准备', '直接准备'),
                                          ('试飞执行', '试飞执行'), ('飞行后讲评', '飞行后讲评'),])
    creator = models.CharField(max_length=20, null=True, verbose_name="创建者")

    class Meta:
        verbose_name = '试飞任务库'
        verbose_name_plural = verbose_name


# 科目危害库
class SubjectHarm(models.Model):
    id = models.AutoField(primary_key=True)
    harm_number = models.CharField(max_length=32, verbose_name="危害编号")  # 危害编号
    change_time = models.DateField(auto_now=True, verbose_name="入库/修改时间")  # 入库/修改时间
    plane_type = models.CharField(max_length=32, verbose_name="所属机型")  # 所属机型
    harm_name = models.CharField(max_length=32, verbose_name="危害名称")  # 危害名称
    applicable_subject = models.CharField(max_length=32, verbose_name="适用科目")  # 适用科目
    R_value = models.CharField(max_length=32, verbose_name="危害评分(R值)")  # 危害评分(R值)
    harm_level = models.CharField(max_length=32, verbose_name="危害等级")  # 危害等级
    subject_type = models.CharField(max_length=32, verbose_name="风险科目类别")  # 风险科目类别
    reason_analysis = models.CharField(max_length=256, verbose_name="原因分析")  # 原因分析
    harm_result = models.CharField(max_length=256, verbose_name="危害后果")  # 危害后果
    counter_measures = models.CharField(max_length=1024, verbose_name="缓解措施")  # 缓解措施，JSONField？
    emergency_response_measures = models.CharField(max_length=32, verbose_name="应急处置措施")  # 应急处置措施
    left_R_value = models.CharField(max_length=32, verbose_name="剩余危害评分(R值)")  # 剩余危害评分(R值)
    left_harm_level = models.CharField(max_length=32, verbose_name="剩余危害等级")  # 剩余危害等级
    remarks = models.CharField(max_length=1024, verbose_name="备注")  # 备注

    class Meta:
        db_table = "SubjectHarm"
        verbose_name = '科目危害库'
        verbose_name_plural = verbose_name


# 危害识别活动库
class SubjectHarmActivity(models.Model):
    id = models.CharField(primary_key=True, max_length=32, verbose_name="编号")  # 编号
    creator = models.CharField(max_length=32, verbose_name="创建人", null=True, blank=True)
    descr = models.CharField(max_length=1024, verbose_name="识别活动描述", null=True, blank=True)  # 识别活动描述
    status = models.CharField(max_length=64, verbose_name="当前识别状态", null=True, blank=True)
    status_activity = models.CharField(max_length=20, null=True, verbose_name="当前活动状态",default='问卷收集中')# 当前活动状态

    class Meta:
        db_table = "SubjectHarmActivity"
        verbose_name = '危害识别活动库'
        verbose_name_plural = verbose_name


# 初步科目危害库（问卷）
class InitialSubjectHarm(models.Model):
    subject = models.CharField(max_length=32, verbose_name="科目")  # 科目
    plane_type = models.CharField(max_length=32, verbose_name="所属机型")  # 所属机型
    harm_name = models.CharField(max_length=32, verbose_name="危害名称")  # 危害名称
    probability = models.CharField(max_length=32, verbose_name="危害发生可能性")  # 该危害发生的可能性有多高？
    seriousness = models.CharField(max_length=32, verbose_name="危害发生严重性")  # 该危害发生的严重性有多高？
    R_value = models.CharField(max_length=32, verbose_name="危害评分")  # 危害评分
    harm_level = models.CharField(max_length=32, verbose_name="危害等级")  # 危害等级
    reason = models.CharField(max_length=128, verbose_name="危害原因")  # 危害原因
    harm_result = models.CharField(max_length=32, verbose_name="危害后果")  # 危害后果
    subject_type = models.CharField(max_length=32, verbose_name="风险科目类别")  # 风险科目类别
    measure1 = models.CharField(max_length=1024, verbose_name="缓解措施")  # 缓解措施
    measure2 = models.CharField(max_length=1024, verbose_name="应急处置措施")  # 应急处置措施
    left_harm_score = models.CharField(max_length=32, verbose_name="剩余危害评分")  # 剩余危害评分
    left_harm_level = models.CharField(max_length=32, verbose_name="剩余危害等级")  # 剩余危害等级
    status = models.CharField(max_length=32, verbose_name="提交状态")  # 提交状态（保存/提交）
    creator = models.CharField(max_length=20, null=True, verbose_name="创建者")# 创建者，从cookie里读出来
    status_activity = models.CharField(max_length=20, null=True, verbose_name="当前问卷状态",default='等待审核')# 当前问卷状态

    fkey = models.ForeignKey('SubjectHarmActivity', on_delete=models.CASCADE)

    # activity = models.ForeignKey('RiskSourceActivity', on_delete=models.CASCADE)

    class Meta:
        db_table = "InitialSubjectHarm"
        verbose_name = '初步科目危害库'
        verbose_name_plural = verbose_name


# 危险源库
class RiskSource(models.Model):
    id = models.CharField(primary_key=True, max_length=32, verbose_name="编号")  # 危险源编号
    change_time = models.DateField(auto_now=True, verbose_name="入库/修改时间")  # 入库/修改时间
    work_stage = models.CharField(max_length=32, verbose_name="工作阶段")  # 工作阶段
    plane_type = models.CharField(max_length=32, verbose_name="所属机型")  # 所属机型
    subject = models.CharField(max_length=32, verbose_name="试飞科目/工作项目")  # 试飞科目/工作项目
    risk_source = models.CharField(max_length=32, verbose_name="危险源")  # 危险源
    risk_source_result = models.CharField(max_length=32, verbose_name="危险源后果")  # 危险源后果
    R_value = models.CharField(max_length=32, verbose_name="风险评分\n(R值)")  # 风险评分(R值)
    risk_level = models.CharField(max_length=32, verbose_name="风险等级")  # 风险等级
    counter_measures = models.CharField(max_length=1024, verbose_name="缓解/控制措施")  # 缓解/控制措施
    derive_R_value = models.CharField(max_length=32, verbose_name="衍生风险评分\n(R值)")  # 衍生风险评分(R值)
    derive_counter_measures = models.CharField(max_length=1024, verbose_name="衍生风险\n缓解措施")  # 衍生风险缓解措施
    left_risk_level = models.CharField(max_length=32, verbose_name="剩余风险等级")  # 剩余风险等级
    approver = models.CharField(max_length=32, verbose_name="风险可接受批准人")  # 风险可接受批准人
    counter_measures_result = models.CharField(max_length=1024, verbose_name="缓解/控制措施落实情况")  # 缓解/控制措施落实情况
    remarks = models.CharField(max_length=1024, verbose_name="备注")  # 备注

    class Meta:
        db_table = "RiskSource"
        verbose_name = '危险源库'
        verbose_name_plural = verbose_name


# 危险源识别活动库
class RiskSourceActivity(models.Model):
    id = models.CharField(primary_key=True, max_length=32, verbose_name="编号")  # 编号
    creator = models.CharField(max_length=32, verbose_name="创建人", null=True, blank=True)
    descr = models.CharField(max_length=1024, verbose_name="识别活动描述", null=True, blank=True)  # 识别活动描述
    status = models.CharField(max_length=64, verbose_name="当前识别状态", null=True, blank=True)
    status_activity = models.CharField(max_length=20, null=True, verbose_name="当前活动状态",default='问卷收集中')# 当前活动状态

    class Meta:
        db_table = "RiskSourceActivity"
        verbose_name = '危险源识别活动库'
        verbose_name_plural = verbose_name


# 初步危险源库（问卷）
class InitialRiskSource(models.Model):
    work_stage = models.CharField(max_length=32, verbose_name="工作阶段")  # 工作阶段
    plane_type = models.CharField(max_length=32, verbose_name="所属机型")  # 所属机型
    department = models.CharField(max_length=32, verbose_name="所属部门")  # 所属部门
    risk_source = models.CharField(max_length=32, verbose_name="危险源")  # 危险源
    risk_source_result = models.CharField(max_length=32, verbose_name="危险源后果")  # 危险源后果
    reason1 = models.CharField(max_length=128, verbose_name="危险原因人的因素")# 危险原因-人
    reason2 = models.CharField(max_length=128, verbose_name="危险原因设备因素")# 危险原因-机
    reason3 = models.CharField(max_length=128, verbose_name="危险原因环境因素")# 危险原因-环境
    reason4 = models.CharField(max_length=128, verbose_name="危险原因管理因素")# 危险原因-管
    R_value = models.CharField(max_length=32, verbose_name="风险评分（R值）")  # 风险评分（R值）
    risk_level = models.CharField(max_length=32, verbose_name="风险等级")  # 风险等级
    counter_measures = models.CharField(max_length=1024, verbose_name="缓解/控制措施")  # 缓解/控制措施
    question_new1 = models.CharField(max_length=32, verbose_name = "新问题1")  # 您负责的流程的工作活动是怎样的?
    question_new2 = models.CharField(max_length=32, verbose_name = "新问题2")  # 请进行该工作活动的系统描述和工作分析
    probability = models.CharField(max_length=128, verbose_name = "危险源发生可能性")  # 该危险源发生的可能性有多高?
    seriousness = models.CharField(max_length=128, verbose_name="危险源发生严重性")# 该危险源发生的严重性有多高?
    left_risk_level = models.CharField(max_length=32, verbose_name="剩余风险等级")# 剩余风险等级
    status = models.CharField(max_length=32, verbose_name="提交状态")  # 提交状态(保存/提交)
    creator = models.CharField(max_length=20, null=True, verbose_name="创建者")# 创建者，从cookie里读出来
    fkey = models.ForeignKey('RiskSourceActivity',on_delete=models.CASCADE)
    status_activity = models.CharField(max_length=20, null=True, verbose_name="当前问卷状态",default='等待审核')# 当前问卷状态

    class Meta:
        db_table = "InitialRiskSource"
        verbose_name = '初步危险源库'
        verbose_name_plural = verbose_name

class RiskSource_By_SubjectHarm(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号")
    risksource = models.ForeignKey('RiskSource',on_delete=models.CASCADE,verbose_name="危险源ID")
    risksource_name = models.CharField(max_length=32, verbose_name="危险源名称")
    subjectharm = models.ForeignKey('SubjectHarm',on_delete=models.CASCADE,verbose_name="危害ID")
    subjectharm_name = models.CharField(max_length=32, verbose_name="危害名称")
    remarks = models.CharField(max_length=1024, verbose_name="备注")  # 备注

    class Meta:
        db_table = "RiskSource_By_SubjectHarm"
        verbose_name = '危险源/危害对应关系库'
        verbose_name_plural = verbose_name


# 专家知识库
class ExpertKnow(models.Model):
    rule_id = models.CharField(max_length=1024,primary_key=True, verbose_name="编号", default=0)#规则编号
    harm_id = models.CharField(max_length=32, verbose_name="危害编号", default=0)  # 危害编号
    harm_name = models.CharField(max_length=32,verbose_name="危害名称", default=0)
    rule_dis = models.CharField(max_length=1024,verbose_name="规则描述", default=0)
    stage = models.CharField(max_length=1024,verbose_name="阶段", default=0)
    para_name = models.CharField(max_length=1024,verbose_name="参数名称", default=0)# 参数名称
    condition = models.CharField(max_length=32,verbose_name="条件", default=0)  # 条件,即比较符号
    reference_val = models.CharField(max_length=32,verbose_name="参考值", default=0)# 参考值
    conclusion = models.CharField(max_length=1024, verbose_name="结论", default=0)  # 结论

    class Meta:
        db_table = "ExpertKnow"
        verbose_name = '专家知识库'
        verbose_name_plural = verbose_name


# 场景库
class Scenario(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="编号")
    name =  models.CharField(max_length=32, verbose_name="场景名称")
    type = models.CharField(max_length=32, verbose_name="场景分类")

    class Meta:
        db_table = "Scenario"
        verbose_name = '场景库'
        verbose_name_plural = verbose_name

## 预测模型参数模板表
# id
# 场景 外键
# ...
# 参数名称
# 参数样式

## 预测任务数据表
# id
# 任务id  外键
# 参数名称
# 参数数值

# 科目库
class Subject(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="科目编号")
    name = models.CharField(max_length=32, verbose_name="科目名称", unique=True)
    major = models.CharField(max_length=64, verbose_name="专业")
    type = models.CharField(max_length=32, verbose_name="科目分类")

    class Meta:
        verbose_name = '科目库'
        verbose_name_plural = verbose_name


# 事前预测活动库
class BeforeFlyActivity(models.Model):
    id = models.CharField(primary_key=True, max_length=32, verbose_name="编号")  # 编号
    creator = models.CharField(max_length=32, verbose_name="创建人", null=True, blank=True)
    descr = models.CharField(max_length=1024, verbose_name="识别活动描述", null=True, blank=True)  # 识别活动描述
    status = models.CharField(max_length=64, verbose_name="当前识别状态", null=True, blank=True)

    class Meta:
        db_table = "BeforeFlyActivity"
        verbose_name = '事前预测活动库'
        verbose_name_plural = verbose_name


# 实时预警活动库
class DuringFlyActivity(models.Model):
    id = models.CharField(primary_key=True, max_length=32, verbose_name="编号")  # 编号
    creator = models.CharField(max_length=32, verbose_name="创建人", null=True, blank=True)
    descr = models.CharField(max_length=1024, verbose_name="识别活动描述", null=True, blank=True)  # 识别活动描述
    status = models.CharField(max_length=64, verbose_name="当前识别状态", null=True, blank=True)

    class Meta:
        db_table = "DuringFlyActivity"
        verbose_name = '实时预警活动库'
        verbose_name_plural = verbose_name