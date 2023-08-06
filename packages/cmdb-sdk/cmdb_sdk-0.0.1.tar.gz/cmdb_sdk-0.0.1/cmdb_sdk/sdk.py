import json

import requests


class CMDBBody:
    def __init__(self):
        self.code = 0
        self.log_id = ""
        self.message = ""
        self.data = None
        self.total = 0
        self.current = 0
        self.pageSize = 20


class CMDBRequest:
    def __init__(self, namespace: str, jwt: str):
        self.http_url_pre = "https://puti-boe.bytedance.net/cmdb/api/"
        # self.http_url_pre = "http://[fdbd:dc02:ff:6:a93:2cd8:0:40b]:6803/cmdb/api/"
        self.version = "v1"
        self.namespace = namespace
        self.jwt = jwt

    def build_v1_router(self, router: str):

        return "{0}/{1}/{2}".format(self.http_url_pre, self.version, router)

    def send_req(self, method, router, body) -> CMDBBody:
        uri = self.build_v1_router(router)
        header = {"Content-Type": "application/json", "PUTI-Namespace": self.namespace, "X-Jwt-Token": self.jwt}
        resp = requests.request(method=method, url=uri, data=json.dumps(body) , headers=header)
        if resp.status_code != 200:
            exception_str = "http code not ok status_code={0}".format(str(resp.status_code))
            raise Exception(exception_str)
        b = resp.json()
        if b["code"] != 0:
            exception_str = "response code not zero code={0} , message={1} , logid={2}".format(str(b["code"]), b["message"],                                                b["logid"])
            raise Exception(exception_str)
        cmdb_body = CMDBBody()
        if not b["response"] is None:
            cmdb_body.data = b["response"]["data"]
            if not b["response"]["total"] :
                cmdb_body.total = b["response"]["total"]
            if not b["response"]["current"] :
                cmdb_body.current = b["response"]["current"]
            if not b["response"]["pageSize"] :
                cmdb_body.pageSize = b["response"]["pageSize"]

        cmdb_body.code = b["code"]
        cmdb_body.log_id = b["logid"]
        cmdb_body.message = b["message"]

        return cmdb_body


class SDK:
    def __init__(self, namespace, jwt_str):
        self.http_req = CMDBRequest(namespace, jwt_str)
        self.namespace = namespace
        self.jwt_str = jwt_str

    def instance_list(self, model_biz_id: str, body) -> CMDBBody:
        router = "instance/list?model_biz_id={0}".format(model_biz_id)
        return self.http_req.send_req("POST", router, body)
