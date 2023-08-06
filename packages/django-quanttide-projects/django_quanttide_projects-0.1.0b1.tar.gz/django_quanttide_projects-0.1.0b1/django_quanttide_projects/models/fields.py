from django.db import models as django_models
from django_quanttide import models

from .choices import (
    ProjectTypeChoices, MatterTypeChoices,
    StatusChoices, PriorityChoices
)


class ProjectTypeField(models.TypeField):
    """
    项目类型字段
    """

    description = "项目类型字段"

    def __init__(self, choices=ProjectTypeChoices.choices, default=ProjectTypeChoices.DEFAULT, **options):
        super().__init__(choices=choices, default=default, **options)


class MatterTypeField(models.TypeField):
    """
    事项类型字段
    """
    description = "事项类型字段"

    def __init__(self, choices=MatterTypeChoices.choices, default=MatterTypeChoices.DEFAULT, **options):
        super().__init__(choices=choices, default=default, **options)


class StatusField(models.StatusField):
    """
    状态字段
    """
    description = "状态字段"

    def __init__(self, choices=StatusChoices.choices, default=StatusChoices.DRAFT, **options):
        super().__init__(choices=choices, default=default, **options)


class PriorityField(django_models.IntegerField):
    """
    优先级字段
    """
    description = "优先级字段"

    def __init__(self, **options):
        options.setdefault('choices', PriorityChoices.choices)
        options.setdefault('default', PriorityChoices.LOW)
        options.setdefault('verbose_name', '优先级')
        super().__init__(**options)
