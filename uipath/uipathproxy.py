from rpa import UIElement
from common import configs
import json
import requests

class UIPathElement(UIElement):
    def execute(self, obj):
        data = json.dumps(obj)
        resp = requests.post(configs["adapter"], data=data)
        if(not resp.ok):
            print(resp)
            raise Exception('failed to connect to the proxy')
        print(resp.json())
        return json.dumps(resp.json())