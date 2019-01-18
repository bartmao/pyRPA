'''
This is a sample to:
    Open notepad, type something and close it
'''
from rpa import UIElement, KeyModifiers, InputMethod
from uipathproxy import UIPathElement
import time

'''
Global settings, add interceptors for ui automations
'''
def beforecall(ins, obj):
    print("Before execution of selector [%s], method [%s]" %(ins.selectorkey, obj['method']))
    ins.highlight(seconds=1, color='green')

def aftercall(ins, obj):
    print("After execution of selector [%s], method [%s]" %(ins.selectorkey, obj['method']))

UIElement.beforecall = beforecall
UIElement.aftercall = aftercall

'''
Start execution
'''

UIPathElement('btn_windows').click(method=InputMethod.Synthesize)
UIPathElement().typetext('notepad')
UIPathElement().sendhotkey('enter', isSpecial=1)
UIPathElement('win_notepad').typetext('This UI automation using Python/UIPath Adapter')
UIPathElement('btn_notepad_close').click()
UIPathElement('btn_notepad_cancel').click()
