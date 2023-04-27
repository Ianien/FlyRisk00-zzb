from django.contrib import admin
from .models import *
import datetime
from .resource import *

from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from django.contrib.admin.models import LogEntry

from import_export.formats import base_formats
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

admin.site.site_header = '实时预警系统后台管理'  # 设置header


class MyImportExportActionModelAdmin(ImportExportActionModelAdmin):
    def export_admin_action(self, request, queryset):
        """
        Exports the selected rows using file_format.
        """
        export_format = request.POST.get('file_format')

        if not export_format:
            messages.warning(request, _('You must select an export format.'))
        else:
            formats = self.get_export_formats()
            file_format = formats[int(export_format)]()

            export_data = self.get_export_data(file_format, queryset, request=request)
            content_type = file_format.get_content_type()
            response = HttpResponse(export_data, content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="%s"' % (
                escape_uri_path(self.get_export_filename(request, queryset, file_format)),
            )
            return response


@admin.register(Scenario)
class ScenarioAdmin(MyImportExportActionModelAdmin):
    resource_class = ScenarioResource
    list_filter = ('id', 'name', 'type')
    list_display = ('id', 'name', 'type')


@admin.register(Subject)
class SubjectAdmin(MyImportExportActionModelAdmin):
    resource_class = SubjectResource
    list_filter = ('id', 'name', 'major', 'type')
    list_display = ('id', 'name', 'major', 'type')


@admin.register(ExpertKnow)
class ExpertKnowAdmin(MyImportExportActionModelAdmin):
    resource_class = ExpertKnowResource
    list_filter = ('rule_id', 'harm_id','harm_name','rule_dis','stage','para_name','condition','reference_val','conclusion')
    list_display = ('rule_id', 'harm_id','harm_name','rule_dis','stage','para_name','condition','reference_val','conclusion')


@admin.register(RiskSource)
class RiskSourceAdmin(MyImportExportActionModelAdmin):
    resource_class = RiskSourceResource
    list_filter = ('id', 'change_time', 'work_stage', 'plane_type',
                   'subject', 'risk_source', 'risk_source_result', 'R_value',
                   'risk_level', 'counter_measures', 'derive_R_value', 'derive_counter_measures',
                   'left_risk_level', 'approver', 'counter_measures_result')
    list_display = ('id', 'change_time', 'work_stage', 'plane_type',
                    'subject', 'risk_source', 'risk_source_result', 'R_value',
                    'risk_level', 'counter_measures', 'derive_R_value', 'derive_counter_measures',
                    'left_risk_level', 'approver', 'counter_measures_result', 'remarks')


@admin.register(SubjectHarm)
class SubjectHarmAdmin(MyImportExportActionModelAdmin):
    resource_class = SubjectHarmResource
    list_filter = ('harm_number', 'change_time', 'plane_type', 'harm_name',
                   'applicable_subject', 'R_value', 'harm_level', 'subject_type',
                   'reason_analysis', 'harm_result', 'counter_measures', 'emergency_response_measures',
                   'left_R_value', 'left_harm_level')
    list_display = ('harm_number', 'change_time', 'plane_type', 'harm_name',
                    'applicable_subject', 'R_value', 'harm_level', 'subject_type',
                    'reason_analysis', 'harm_result', 'counter_measures', 'emergency_response_measures',
                    'left_R_value', 'left_harm_level', 'remarks')


@admin.register(admin.models.LogEntry)
class LogEntryAdmin(MyImportExportActionModelAdmin):
    list_display_links = None
    list_filter = ('action_time', 'user', 'content_type','action_flag')
    list_display = ['action_time', 'user', 'content_type', '__str__','action_flag']

    def has_add_permission(self, request):
        return False

    def get_export_formats(self):  # 该方法是限制格式
        formats = (
            base_formats.XLS,base_formats.XLSX
        )
        return [f for f in formats if f().can_export()]

    def get_import_formats(self):  # 该方法是限制格式
        formats = (
            base_formats.XLS,base_formats.XLSX

        )
        return [f for f in formats if f().can_import()]

    def has_import_permission(self, request):
        return False

    def get_export_filename(self, request, queryset, file_format):
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = "%s-%s.%s" % ('日志记录',
                                 date_str,
                                 file_format.get_extension())
        return filename


# @admin.register(FlyTask)
# class FlyTaskAdmin(MyImportExportActionModelAdmin):
#     resource_class = FTResource
#     list_filter = ('task_number', 'tabll', 'machine_number', 'edit_time',
#                    'risk_level', 'project_name', 'task', 'subject',
#                    'distribute_time', 'exe_status', 'creator')
#     list_display = ('task_number', 'tabll', 'machine_number', 'edit_time',
#                    'risk_level', 'project_name', 'task', 'subject',
#                    'distribute_time', 'exe_status', 'creator')