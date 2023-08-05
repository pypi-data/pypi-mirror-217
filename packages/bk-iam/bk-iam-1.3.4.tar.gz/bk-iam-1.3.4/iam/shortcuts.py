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

from . import Request
from .exceptions import AuthFailedException


def allow_or_raise_auth_failed(iam, system, subject, action, resources, environment=None, cache=False):
    request = Request(system, subject, action, resources, environment)

    allowed = iam.is_allowed_with_cache(request) if cache else iam.is_allowed(request)

    if not allowed:
        raise AuthFailedException(system, subject, action, resources)

    return
