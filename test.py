from android.droidagent import DroidAdapter, DroidElement
from uipathproxy import UIPathElement
from rpa import InputMethod
import os.path

agent = DroidAdapter()
e = agent.readelement("<andriod resource-id='com.android.contacts:id/searchbarleft'/>")
print(e)