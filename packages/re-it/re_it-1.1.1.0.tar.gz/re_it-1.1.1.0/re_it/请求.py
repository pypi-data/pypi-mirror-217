import http.client

class 我的请求:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/json'
        }

    def 添加头部(self, 键, 值):
        self.headers[键] = 值

    def 获取(self, 网址):
        conn = http.client.HTTPSConnection(网址)
        conn.request("GET", "/", headers=self.headers)
        response = conn.getresponse()
        响应内容 = response.read().decode()
        conn.close()
        return 响应内容

    def 提交(self, 网址, 数据=None):
        conn = http.client.HTTPSConnection(网址)
        conn.request("POST", "/", body=数据, headers=self.headers)
        response = conn.getresponse()
        响应内容 = response.read().decode()
        conn.close()
        return 响应内容
