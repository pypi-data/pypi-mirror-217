"""
数据模型
"""

from django.db import models

from .fields import IDField


class Model(models.Model):
    """
    量潮Django Model类

    使用UUID代替integer自增字段作为默认ID字段。
    """
    id = IDField()

    class Meta:
        abstract = True
