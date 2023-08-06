import requests
import json
from xesai.chat import sseclient
import sys

class Robot():
    def __init__(self):
        self.authorization = self._getAuthorization()
        
    def ask(self, prompt, history=[], max_tokens=0):
        stream = False
        url = "https://codeapi.xueersi.com/ai/aigc/v2/chat"
        data = json.dumps({
            "prompt": prompt, 
            "history": history,
            "stream": stream,
            "max_tokens": max_tokens,
        })
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.authorization
        }
        response = requests.post(url, stream=stream, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]["message"]["content"]
        else:
            raise Exception("请求失败，错误码：" + str(response.status_code))
    
    def ask_stream(self, prompt, history=[], max_tokens=0):
        stream = True
        url = "https://codeapi.xueersi.com/ai/aigc/v2/chat"
        data = json.dumps({
            "prompt": prompt, 
            "history": history,
            "stream": stream,
            "max_tokens": max_tokens,
        })
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.authorization
        }
        response = requests.post(url, stream=stream, data=data, headers=headers)
        if response.status_code == 200:
            client = sseclient.SSEClient(response)
            return Stream(client)
        else:
            raise Exception("请求失败，错误码：" + str(response.status_code))
        
    def _getAuthorization(self):
        # Python离线和Python在线的用这个接口换取token
        url = "https://code.xueersi.com/api/ai/auth_by_run_token"
        
        # js的webpy和scratch的用这个接口换取token
        # url = "https://code.xueersi.com/api/ai/auth"
        
        cookies = self._getRunCookies()
        headers = {
            "Cookie": cookies,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return "Bearer " + response.json()["data"]["token"]
            
    def _getRunCookies(self):
        cookies = ""
        if len(sys.argv) > 1:
            try:
                cookies = json.loads(sys.argv[1])["cookies"]
            except:
                pass
        return cookies
        
class Stream():
    def __init__(self, client):
        self.client = client
        
    def contents(self):
        for event in self.client.events():
            if event.event == "message":
                data = json.loads(event.data)
                content = data["message"]["content"]
                yield content
