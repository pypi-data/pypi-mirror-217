from django_quanttide import models

from .fields import ProjectTypeField, StatusField, PriorityField


class BaseProject(models.Model):
    """
    项目模型基类
    """
    name = models.NameField()
    title = models.TitleField()
    description = models.DescriptionField()
    type = ProjectTypeField()
    status = StatusField()
    priority = PriorityField()
    created_at = models.CreatedAtField()
    updated_at = models.UpdatedAtField()

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目列表'
        abstract = True
