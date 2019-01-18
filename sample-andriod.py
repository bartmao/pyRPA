from android.droidagent import DroidAdapter, DroidElement
from uipathproxy import UIPathElement
from rpa import InputMethod
import time

'''
 A sample can open contact book and search the phone number by specific name
'''
agent = DroidAdapter()
DroidElement.setAgent(agent)
person = 'Bart'
DroidElement().start('contacts')
time.sleep(1)
DroidElement('txt_contact_search').click()
DroidElement().typetext(person)
DroidElement('txt_contact_search_first').click()
phone = DroidElement('txt_contact_details').gettext()
print('%s\'Phone Number is %s'%(person, phone))