from django.db import models


class ProjectTypeChoices(models.TextChoices):
    """
    项目类型选项
    """
    DEFAULT = 'default', '项目'
    PROGRAM = 'program', '项目集'
    PROJECT_PORTFOLIO = 'project_portfolio', '项目组合'


class MatterTypeChoices(models.TextChoices):
    """
    事项类型选项
    """
    DEFAULT = 'default', '事项'
    MILLSTONE = 'millstone', '里程碑'
    EPIC = 'epic', '史诗'
    STORY = 'story', '用户故事'
    TASK = 'task', '任务'
    DEFECT = 'defect', '缺陷'


class PriorityChoices(models.IntegerChoices):
    """
    优先级选项

    类似于logging模块的level选项的设计风格。使用形容词描述。
    """
    LOW = 10, '低'
    MIDDLE = 20, '中'
    HIGH = 30, '高'
    URGENT = 40, '紧急'


class StatusChoices(models.TextChoices):
    """
    状态选项

    遵循项目和事项的生命周期的定义，使用形容词或动名词描述。
    """
    DRAFT = 'drafting', '起草中'
    EVALUATION = 'evaluating', '评估中'
    AWAITING = 'awaiting', '等待开始'
    IN_PROGRESS = 'in_progress', '进行中'
    DELAYED = 'delayed', '已延迟'
    PAUSED = 'paused', '已暂停'
    REVIEWING = 'reviewing', '评审中'
    DELIVERING = 'delivering', '交付中'
    SUMMARIZING = 'summarizing', '复盘中'
    COMPLETED = 'completed', '已完成'
    CANCELLED = 'cancelled', '已取消'
