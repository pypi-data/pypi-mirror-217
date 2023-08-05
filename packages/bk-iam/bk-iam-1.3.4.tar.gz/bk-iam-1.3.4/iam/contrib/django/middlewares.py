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


from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

from iam.contrib.django.response import IAMAuthFailedResponse
from iam.exceptions import AuthFailedBaseException


class AuthFailedExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, AuthFailedBaseException):
            api_prefix = getattr(settings, "BK_IAM_API_PREFIX", "")
            status_code = 200 if api_prefix and request.path.startswith(api_prefix) else 499
            return IAMAuthFailedResponse(exception, status=status_code)
