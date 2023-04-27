from import_export import resources
from import_export.fields import Field
from .models import *


class ChineseModelResource(resources.ModelResource):
    @classmethod
    def field_from_django_field(cls, field_name, django_field, readonly):
        FieldWidget = cls.widget_from_django_field(django_field)
        widget_kwargs = cls.widget_kwargs_for_field(field_name)
        field = cls.DEFAULT_RESOURCE_FIELD(
            attribute=field_name,
            # 重写column_name
            column_name=django_field.verbose_name,
            widget=FieldWidget(**widget_kwargs),
            readonly=readonly,
            default=django_field.default,
        )
        return field


class FTResource(ChineseModelResource):
    class Meta:
        model = FlyTask

    def __init__(self):
        super(FTResource, self).__init__()

        field_list = FlyTask._meta.fields
        self.vname_dict = {}
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name

    def get_export_fields(self):
        fields = self.get_fields()
        for i, field in enumerate(fields):
            field_name = self.get_field_name(field)
            if field_name.find("__") > 0:
                _field_name = field_name.split("__")[0]
                if _field_name in self.vname_dict.keys():
                    field.column_name = self.vname_dict[_field_name]
            elif field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    def get_import_fields(self):
        fields = self.get_fields()
        for i, field in enumerate(fields):
            field_name = self.get_field_name(field)
            if field_name.find("__") > 0:
                _field_name = field_name.split("__")[0]
                if _field_name in self.vname_dict.keys():
                    field.column_name = self.vname_dict[_field_name]
            elif field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields


class SubjectHarmResource(ChineseModelResource):
    class Meta:
        import_id_fields = ['id']
        model = SubjectHarm

    def __init__(self):
        super(SubjectHarmResource, self).__init__()

        field_list = SubjectHarm._meta.fields
        self.vname_dict = {}
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name

    def get_export_fields(self):
        fields = self.get_fields()
        for i, field in enumerate(fields):
            field_name = self.get_field_name(field)
            if field_name.find("__") > 0:
                _field_name = field_name.split("__")[0]
                if _field_name in self.vname_dict.keys():
                    field.column_name = self.vname_dict[_field_name]
            elif field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    def get_import_fields(self):
        fields = self.get_fields()
        for i, field in enumerate(fields):
            field_name = self.get_field_name(field)
            if field_name.find("__") > 0:
                _field_name = field_name.split("__")[0]
                if _field_name in self.vname_dict.keys():
                    field.column_name = self.vname_dict[_field_name]
            elif field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields


class RiskSourceResource(ChineseModelResource):
    class Meta:
        model = RiskSource
        import_id_fields = ['id']

    def __init__(self):
        super(RiskSourceResource, self).__init__()

        field_list = RiskSource._meta.fields
        print(field_list)
        self.vname_dict = {}
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name

    def get_export_fields(self):
        fields = self.get_fields()
        for i, field in enumerate(fields):
            field_name = self.get_field_name(field)
            if field_name.find("__") > 0:
                _field_name = field_name.split("__")[0]
                if _field_name in self.vname_dict.keys():
                    field.column_name = self.vname_dict[_field_name]
            elif field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    def get_import_fields(self):
        fields = self.get_fields()
        for i, field in enumerate(fields):
            field_name = self.get_field_name(field)
            if field_name.find("__") > 0:
                _field_name = field_name.split("__")[0]
                if _field_name in self.vname_dict.keys():
                    field.column_name = self.vname_dict[_field_name]
            elif field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields


class ExpertKnowResource(ChineseModelResource):
    class Meta:
        model = ExpertKnow
        # exclude = ('id',)
        # import_id_fields = ['bearing_code']
        # fields = ('bearing_code', 'bearing_name')

    def __init__(self):
        super(ExpertKnowResource, self).__init__()

        field_list = ExpertKnow._meta.fields
        self.vname_dict = {}
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name

    def get_export_fields(self):
        fields = self.get_fields()
        for i, field in enumerate(fields):
            field_name = self.get_field_name(field)
            if field_name.find("__") > 0:
                _field_name = field_name.split("__")[0]
                if _field_name in self.vname_dict.keys():
                    field.column_name = self.vname_dict[_field_name]
            elif field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    def get_import_fields(self):
        fields = self.get_fields()
        for i, field in enumerate(fields):
            field_name = self.get_field_name(field)
            if field_name.find("__") > 0:
                _field_name = field_name.split("__")[0]
                if _field_name in self.vname_dict.keys():
                    field.column_name = self.vname_dict[_field_name]
            elif field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields


class ScenarioResource(ChineseModelResource):
    class Meta:
        model = Scenario
        # exclude = ('id',)
        # import_id_fields = ['bearing_code']
        # fields = ('bearing_code', 'bearing_name')

    def __init__(self):
        super(ScenarioResource, self).__init__()

        field_list = Scenario._meta.fields
        self.vname_dict = {}
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name

    def get_export_fields(self):
        fields = self.get_fields()
        for i, field in enumerate(fields):
            field_name = self.get_field_name(field)
            if field_name.find("__") > 0:
                _field_name = field_name.split("__")[0]
                if _field_name in self.vname_dict.keys():
                    field.column_name = self.vname_dict[_field_name]
            elif field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    def get_import_fields(self):
        fields = self.get_fields()
        for i, field in enumerate(fields):
            field_name = self.get_field_name(field)
            if field_name.find("__") > 0:
                _field_name = field_name.split("__")[0]
                if _field_name in self.vname_dict.keys():
                    field.column_name = self.vname_dict[_field_name]
            elif field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields


class SubjectResource(ChineseModelResource):
    class Meta:
        model = Subject
        # exclude = ('id',)
        # import_id_fields = ['bearing_code']
        # fields = ('bearing_code', 'bearing_name')

    def __init__(self):
        super(SubjectResource, self).__init__()

        field_list = Subject._meta.fields
        self.vname_dict = {}
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name

    def get_export_fields(self):
        fields = self.get_fields()
        for i, field in enumerate(fields):
            field_name = self.get_field_name(field)
            if field_name.find("__") > 0:
                _field_name = field_name.split("__")[0]
                if _field_name in self.vname_dict.keys():
                    field.column_name = self.vname_dict[_field_name]
            elif field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    def get_import_fields(self):
        fields = self.get_fields()
        for i, field in enumerate(fields):
            field_name = self.get_field_name(field)
            if field_name.find("__") > 0:
                _field_name = field_name.split("__")[0]
                if _field_name in self.vname_dict.keys():
                    field.column_name = self.vname_dict[_field_name]
            elif field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields
