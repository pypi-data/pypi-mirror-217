# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云-权限中心Python SDK(iam-python-sdk) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import abc

import six

from iam.resource.constants import SchemaSpecificType


class ListResult(object):
    def __init__(self, results, count):
        """
        :param results: 返回的结果
        :param count: 总记录数
        """
        self.count = count
        self.results = results

    def to_dict(self):
        return {"count": self.count, "results": self.results}

    def to_list(self):
        return self.results


class SchemaResult(object):
    def __init__(self, properties):
        """
        :param properties: 资源类型 schema 定义
        """
        self.type = SchemaSpecificType.OBJECT
        self.properties = properties

    def to_dict(self):
        return {"type": self.type, "properties": self.properties}


@six.add_metaclass(abc.ABCMeta)
class ResourceProvider(object):
    @abc.abstractmethod
    def list_attr(self, **options):
        """
        处理来自 iam 的 list_attr 请求
        return: ListResult
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def list_attr_value(self, filter, page, **options):
        """
        处理来自 iam 的 list_attr_value 请求
        return: ListResult
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def list_instance(self, filter, page, **options):
        """
        处理来自 iam 的 list_instance 请求
        return: ListResult
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def fetch_instance_info(self, filter, **options):
        """
        处理来自 iam 的 fetch_instance_info 请求
        return: ListResult
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def list_instance_by_policy(self, filter, page, **options):
        """
        处理来自 iam 的 list_instance_by_policy 请求
        return: ListResult
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def search_instance(self, filter, page, **options):
        """
        处理来自 iam 的 search_instance 请求
        return: ListResult
        """
        raise NotImplementedError()

    def fetch_instance_list(self, filter, page, **options):
        """
        处理来自 iam 的 fetch_instance_list 请求
        在审计中心生成静态资源快照时，需要实现此方法
        return: ListResult
        """
        raise NotImplementedError()

    def fetch_resource_type_schema(self, **options):
        """
        处理来自 iam 的 fetch_resource_type_schema 请求
        在审计中心显示静态资源时，需要实现此方法
        return: SchemaResult
        """
        raise NotImplementedError()
