from andriod.driodagent import DriodAgent
from common import trace, configs
import subprocess
import time
import re
import xml.etree.ElementTree
#subprocess.call(['echo', 'hello'], shell=True)

ag = DriodAgent()
b = "<andriod text='通讯录' class='android.widget.TextView' package='com.tencent.mm' />"
ag.execute(b)