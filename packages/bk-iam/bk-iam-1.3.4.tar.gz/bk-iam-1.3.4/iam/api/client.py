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


from __future__ import unicode_literals

import json
import logging
import os
import time

from cachetools import TTLCache, cached
from requests.models import PreparedRequest

from iam.exceptions import AuthAPIError
from .http import http_delete, http_get, http_post, http_put

logger = logging.getLogger("iam")

BK_IAM_VERSION = "1"


class Client(object):
    """
    input: json
    """

    def __init__(self, app_code, app_secret, bk_iam_host=None, bk_paas_host=None, bk_apigateway_url=None):
        """
        如果有 APIGateway 且权限中心网关接入, 则可以统一API请求全部走APIGateway
        - 没有APIGateway的用法: Client(app_code, app_secret, bk_iam_host, bk_paas_host)
        - 有APIGateway的用法: Client(app_code, app_secret, bk_apigateway_url)

        NOTE: 未来将会下线`没有 APIGateway的用法`
        """
        self._app_code = app_code
        self._app_secret = app_secret

        # enabled apigateway
        self._apigateway_on = False
        if bk_apigateway_url:
            self._apigateway_on = True
            # replace the host
            self._host = bk_apigateway_url.rstrip("/")
        else:
            if not (bk_iam_host and bk_paas_host):
                raise AuthAPIError("init client fail, bk_iam_host and bk_paas_host should not be empty")

            self._host = bk_iam_host
            self._bk_paas_host = bk_paas_host

        # will add ?debug=true in url, for debug api/policy, show the details
        is_api_debug_enabled = (
            os.environ.get("IAM_API_DEBUG") == "true" or os.environ.get("BKAPP_IAM_API_DEBUG") == "true"
        )
        # will add ?force=true in url, for api/policy run without cache(all data from database)
        is_api_force_enabled = (
            os.environ.get("IAM_API_FORCE") == "true" or os.environ.get("BKAPP_IAM_API_FORCE") == "true"
        )

        self._extra_url_params = {}
        if is_api_debug_enabled:
            self._extra_url_params["debug"] = "true"
        if is_api_force_enabled:
            self._extra_url_params["force"] = "true"

    def _call_api(self, http_func, host, path, data, headers, timeout=None):
        url = "{host}{path}".format(host=host, path=path)

        begin = time.time()

        # add extra params in url if not empty
        if self._extra_url_params:
            preReq = PreparedRequest()
            preReq.prepare_url(url, self._extra_url_params)
            url = preReq.url

        ok, message, _data = http_func(url, data, headers=headers, timeout=timeout)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("do http request: method=`%s`, url=`%s`, data=`%s`", http_func.__name__, url, json.dumps(data))
            logger.debug("http request result: ok=`%s`, message=`%s`, _data=`%s`", ok, message, json.dumps(_data))
            logger.debug("http request took %s ms", int((time.time() - begin) * 1000))

        if not ok:
            return False, message or "request to iam server fail", None

        if _data.get("code") != 0:
            return False, _data.get("message") or "iam api fail", None

        _d = _data.get("data")
        return True, "ok", _d

    def _call_apigateway_api(self, http_func, path, data, timeout=None):
        """
        统一后, 所有接口调用走APIGateway
        """
        headers = {
            "X-Bkapi-Authorization": json.dumps({"bk_app_code": self._app_code, "bk_app_secret": self._app_secret}),
            "X-Bk-IAM-Version": BK_IAM_VERSION,
        }
        return self._call_api(http_func, self._host, path, data, headers, timeout=timeout)

    def _call_iam_api(self, http_func, path, data, timeout=None):
        """
        兼容切换到apigateway, 统一后, 这个方法应该去掉
        """
        if self._apigateway_on:
            return self._call_apigateway_api(http_func, path, data, timeout)

        # call directly
        headers = {
            "X-BK-APP-CODE": self._app_code,
            "X-BK-APP-SECRET": self._app_secret,
            "X-Bk-IAM-Version": BK_IAM_VERSION,
        }

        return self._call_api(http_func, self._host, path, data, headers, timeout=timeout)

    def _call_esb_api(self, http_func, path, data, bk_token, bk_username, timeout=None):
        """
        兼容切换到apigateway, 统一后, 这个方法应该去掉
        """
        if self._apigateway_on:
            apigw_path = path.replace("/api/c/compapi/v2/iam/", "/api/v1/open/")
            if not apigw_path.startswith("/api/v1/open/"):
                raise AuthAPIError("can't find the matched apigateway path, the esb api path is %s" % path)

            return self._call_apigateway_api(http_func, apigw_path, data, timeout)

        # call esb
        headers = {}
        data.update(
            {
                "bk_app_code": self._app_code,
                "bk_app_secret": self._app_secret,
                "bk_token": bk_token,
                "bk_username": bk_username,
            }
        )
        return self._call_api(http_func, self._bk_paas_host, path, data, headers, timeout=timeout)

    # ---------- system
    def add_system(self, data):
        # data.id required
        path = "/api/v1/model/systems"
        ok, message, data = self._call_iam_api(http_post, path, data)
        # if alreay exists, return true
        return ok, message

    def update_system(self, system_id, data):
        # data.id required
        path = "/api/v1/model/systems/{system_id}".format(system_id=system_id)
        ok, message, data = self._call_iam_api(http_put, path, data)
        return ok, message

    # ---------- resource_type
    def batch_add_resource_types(self, system_id, data):
        path = "/api/v1/model/systems/{system_id}/resource-types".format(system_id=system_id)
        ok, message, data = self._call_iam_api(http_post, path, data)
        # if alreay exists, return true
        return ok, message

    def update_resource_type(self, system_id, resource_type_id, data):
        path = "/api/v1/model/systems/{system_id}/resource-types/{resource_type_id}".format(
            system_id=system_id, resource_type_id=resource_type_id
        )

        ok, message, data = self._call_iam_api(http_put, path, data)
        return ok, message

    def batch_delete_resource_types(self, system_id, data):
        path = "/api/v1/model/systems/{system_id}/resource-types?check_existence=false".format(system_id=system_id)
        ok, message, data = self._call_iam_api(http_delete, path, data)
        return ok, message

    # ---------- action
    def batch_add_actions(self, system_id, data):
        path = "/api/v1/model/systems/{system_id}/actions".format(system_id=system_id)
        ok, message, data = self._call_iam_api(http_post, path, data)
        return ok, message

    def update_action(self, system_id, action_id, data):
        path = "/api/v1/model/systems/{system_id}/actions/{action_id}".format(system_id=system_id, action_id=action_id)
        ok, message, data = self._call_iam_api(http_put, path, data)
        return ok, message

    def batch_delete_actions(self, system_id, data):
        path = "/api/v1/model/systems/{system_id}/actions?check_existence=false".format(system_id=system_id)
        ok, message, data = self._call_iam_api(http_delete, path, data)
        return ok, message

    # register create association permission action.
    def add_resource_creator_actions(self, system_id, data):
        path = "/api/v1/model/systems/{system_id}/configs/resource_creator_actions".format(system_id=system_id)
        ok, message, data = self._call_iam_api(http_post, path, data)
        return ok, message

    # update create association permission action.
    def update_resource_creator_actions(self, system_id, data):
        path = "/api/v1/model/systems/{system_id}/configs/resource_creator_actions".format(system_id=system_id)
        ok, message, data = self._call_iam_api(http_put, path, data)
        return ok, message

    # return resource instance creator to iam, esb needed.
    def grant_resource_creator_actions(self, bk_token, bk_username, data):
        path = "/api/c/compapi/v2/iam/authorization/resource_creator_action/"

        ok, message, _data = self._call_esb_api(http_post, path, data, bk_token, bk_username, timeout=5)
        if not ok:
            return False, message

        return True, "success"

    # return resource instance creator action attribute to iam, esb needed.
    def grant_resource_creator_action_attributes(self, bk_token, bk_username, data):
        path = "/api/c/compapi/v2/iam/authorization/resource_creator_action_attribute/"

        ok, message, data = self._call_esb_api(http_post, path, data, bk_token, bk_username, timeout=5)
        if not ok:
            return False, message

        return True, "success"

    # return resource instance creator to iam, esb needed.
    def grant_batch_resource_creator_actions(self, bk_token, bk_username, data):
        path = "/api/c/compapi/v2/iam/authorization/batch_resource_creator_action/"

        ok, message, _data = self._call_esb_api(http_post, path, data, bk_token, bk_username, timeout=5)
        if not ok:
            return False, message

        return True, "success"

    # ---------- action-topology
    def add_action_topology(self, system_id, action_type, data):
        path = "/api/v1/model/systems/{system_id}/action-topologies/{action_type}".format(
            system_id=system_id, action_type=action_type
        )
        ok, message, data = self._call_iam_api(http_post, path, data)
        # if alreay exists, return true
        return ok, message

    def update_action_topology(self, system_id, action_type, data):
        path = "/api/v1/model/systems/{system_id}/action-topologies/{action_type}".format(
            system_id=system_id, action_type=action_type
        )
        ok, message, data = self._call_iam_api(http_put, path, data)
        # if alreay exists, return true
        return ok, message

    # ---------- query
    def query(self, system_id):
        path = "/api/v1/model/systems/{system_id}/query".format(system_id=system_id)
        ok, message, data = self._call_iam_api(http_get, path, None)
        return ok, message, data

    # ---------- ping
    def ping(self):
        url = "{host}{path}".format(host=self._host, path="/ping")
        ok, _, data = http_get(url, None, timeout=5)
        return ok, data

    # ---------- query system_id_set/resource_type_id_set, action_id_set
    @cached(cache=TTLCache(maxsize=10, ttl=30))
    def query_all_models(self, system_id):
        ok, message, data = self.query(system_id)
        if not ok:
            return set(), set(), set()

        system = data.get("base_info", {})
        resource_types = data.get("resource_types", [])
        actions = data.get("actions", [])

        system_id_set = {system.get("id")}
        resource_type_id_set = {r.get("id") for r in resource_types}
        action_id_set = {a.get("id") for a in actions}

        return system_id_set, resource_type_id_set, action_id_set

    # --------- upset
    def upsert_system(self, system_id, data):
        system_id_set, _, _ = self.query_all_models(system_id)

        if system_id not in system_id_set:
            return self.add_system(system_id, data)
        return self.update_system(system_id, data)

    def upsert_resource_type(self, system_id, data):
        # data.id required
        d_resource_type_id = data.get("id")
        if not d_resource_type_id:
            return False, "the field `id` required"

        _, resource_id_set, _ = self.query_all_models(system_id)

        if d_resource_type_id not in resource_id_set:
            return self.add_resource_type(system_id, data)
        return self.update_resource_type(system_id, data)

    def upsert_action(self, system_id, data):
        d_action_id = data.get("id")
        if not d_action_id:
            return False, "the field `id` required"

        _, _, action_id_set = self.query_all_models(system_id)

        if d_action_id not in action_id_set:
            return self.add_action(system_id, data)
        return self.update_action(system_id, data)

    # --------- policy
    def policy_query(self, data):
        path = "/api/v1/policy/query"
        ok, message, data = self._call_iam_api(http_post, path, data)
        return ok, message, data

    # --------- policy v2
    def v2_policy_query(self, system_id, data):
        path = f"/api/v2/policy/systems/{system_id}/query/"
        ok, message, data = self._call_iam_api(http_post, path, data)
        return ok, message, data

    def policy_query_by_actions(self, data):
        path = "/api/v1/policy/query_by_actions"
        ok, message, data = self._call_iam_api(http_post, path, data)
        return ok, message, data

    def v2_policy_query_by_actions(self, system_id, data):
        path = f"/api/v2/policy/systems/{system_id}/query_by_actions/"
        ok, message, data = self._call_iam_api(http_post, path, data)
        return ok, message, data

    def get_token(self, system_id):
        path = "/api/v1/model/systems/{system_id}/token".format(system_id=system_id)
        ok, message, _data = self._call_iam_api(http_get, path, {})
        if not ok:
            return False, message, ""

        return True, "success", _data.get("token", "")

    # apply
    def get_apply_url(self, bk_token, bk_username, data):
        path = "/api/c/compapi/v2/iam/application/"

        ok, message, _data = self._call_esb_api(http_post, path, data, bk_token, bk_username, timeout=5)
        if not ok:
            return False, message, ""

        return True, "success", _data.get("url", "")

    def instance_authorization(self, bk_token, bk_username, data):
        path = "/api/c/compapi/v2/iam/authorization/instance/"
        ok, message, _data = self._call_esb_api(http_post, path, data, bk_token, bk_username, timeout=5)
        if not ok:
            return False, message, ""
        return True, "success", _data.get("token", "")

    def batch_instance_authorization(self, bk_token, bk_username, data):
        path = "/api/c/compapi/v2/iam/authorization/batch_instance/"
        ok, message, _data = self._call_esb_api(http_post, path, data, bk_token, bk_username, timeout=5)
        if not ok:
            return False, message, ""
        return True, "success", _data

    def path_authorization(self, bk_token, bk_username, data):
        path = "/api/c/compapi/v2/iam/authorization/path/"
        ok, message, _data = self._call_esb_api(http_post, path, data, bk_token, bk_username, timeout=5)
        if not ok:
            return False, message, ""
        return True, "success", _data.get("token", "")

    def batch_path_authorization(self, bk_token, bk_username, data):
        path = "/api/c/compapi/v2/iam/authorization/batch_path/"
        ok, message, _data = self._call_esb_api(http_post, path, data, bk_token, bk_username, timeout=5)
        if not ok:
            return False, message, ""
        return True, "success", _data

    def query_policies_with_action_id(self, system_id, data):
        path = "/api/v1/systems/{system_id}/policies".format(system_id=system_id)
        ok, message, data = self._call_iam_api(http_get, path, data)
        if not ok:
            return False, message, ""
        return True, message, data
