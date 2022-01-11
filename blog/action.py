# coding: utf-8
"""
Created by Jeyrce.Lu at 2019/03/16 16:41, for any questions contact me with jeyrce@gmail.com.
Some ideas of the file:
    0. 自定义action
"""
from django.core.exceptions import PermissionDenied
from xadmin.views.base import filter_hook
from xadmin.plugins.actions import BaseActionView


class ActiveSelectedAction(BaseActionView):
    action_name = "active_selected"
    description = "激活/启用-所选项"

    model_perm = 'change'
    icon = 'fa fa-times'

    @filter_hook
    def do_action(self, queryset):
        # Check that the user has change permission for the actual model
        if not self.has_change_permission():
            raise PermissionDenied
        queryset.update(is_active=True)


class BlockSelectedAction(BaseActionView):
    action_name = "block_selected"
    description = "禁用/隐藏-所选项"

    model_perm = 'change'
    icon = 'fa fa-times'

    @filter_hook
    def do_action(self, queryset):
        # Check that the user has change permission for the actual model
        if not self.has_change_permission():
            raise PermissionDenied
        queryset.update(is_active=False)
