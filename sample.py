'''
This is a sample to:
    Open notepad, type something and close it
'''
from rpa import uielement, KeyModifiers, InputMethod
import time

'''
Global settings, add interceptors for ui automations
'''
def beforecall(ins, obj):
    print("Before execution of selector [%s], method [%s]" %(ins.selectorkey, obj['method']))
    ins.highlight(seconds=1, color='green')

def aftercall(ins, obj):
    print("After execution of selector [%s], method [%s]" %(ins.selectorkey, obj['method']))

uielement.beforecall = beforecall
uielement.aftercall = aftercall

'''
Start execution
'''

uielement('btn_windows').click(method=InputMethod.Synthesize)
uielement().typetext('notepad')
uielement().sendhotkey('enter', isSpecial=1)
uielement('win_notepad').typetext('This UI automation using Python/UIPath Adapter')
uielement('btn_notepad_close').click()
uielement('btn_notepad_cancel').click()