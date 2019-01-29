# pyRPA
A RPA framework automated by Python, can also integrated with other RPA tools, like UIPath. Currently support
1. Desktop/Broswer automation driven by UIPath (RPA.UIPathAdapter)
2. Desktop/Broswer automation driven by Python code (In Progressing...)
3. Android automation

The main idea I use python to do RPA because:
1. Pure code is easier to maintain compared to auto-generated code by the RPA designers
2. Can easily do the interception things
3. Can easily cross platform

## Setup
Using UIPath
1. Checkout file [pyRPA/RPA.UIPathAdapter/binary/RPA.UIPathAdapter.exe.config], update `UIPathActFolder` to your own uipath folder
2. Run adapter pyRPA/RPA.UIPathAdapter/binary/RPA.UIPathAdapter.exe under administrator permission 

Using Andriod
1. Install adb
2. Install android SDK(optional, we can use <android sdk>/uiautomator to inspect elements)

## Sample driven by UIPath (samples/sample.py)

This sample will automatically open notepad, type something and close it. 
1. It will create logs before and after each UI automation
2. It will highlight the element to be operated

![1](https://user-images.githubusercontent.com/4489728/51222515-0bba3280-1979-11e9-9a9d-d77e718f1d1a.gif)
Output:
```code
Before execution of selector [btn_windows], method [click]
After execution of selector [btn_windows], method [click]
Before execution of selector [], method [typetext]
After execution of selector [], method [typetext]
Before execution of selector [], method [sendhotkey]
After execution of selector [], method [sendhotkey]
Before execution of selector [win_notepad], method [typetext]
After execution of selector [win_notepad], method [typetext]
Before execution of selector [btn_notepad_close], method [click]
After execution of selector [btn_notepad_close], method [click]
Before execution of selector [btn_notepad_cancel], method [click]
After execution of selector [btn_notepad_cancel], method [click]
```

## Sample on Android (samples/sample-andriod.py)
This sample will search specific contact and print the phone number for you

![1](https://user-images.githubusercontent.com/4489728/51382853-d701d300-1b52-11e9-8d34-b3d82716dc8f.gif)
Output:
```code
PS C:\Users\bmao002\Desktop\Projects\pyRPA> python .\sample-andriod.py
{"selector": "", "method": "start", "args": {"app": "contacts"}, "attrs": {}}
Warning: Activity not started, its current task has been brought to the front
{"selector": "<andriod resource-id='com.android.contacts:id/searchbarleft'/>", "method": "click", "args": {"type": 0, "button": 0, "pos": 4, "method": 2}, "attrs": {}}
.//node[@resource-id="com.android.contacts:id/searchbarleft"]
performing click @[241.0, 303.0]
{"selector": "", "method": "typetext", "args": {"text": "Bart", "method": 1}, "attrs": {}}
performing typing
{"selector": "<andriod resource-id='com.android.contacts:id/name'/>", "method": "click", "args": {"type": 0, "button": 0, "pos": 4, "method": 2}, "attrs": {}}
performing click @[411.0, 392.5]
{"selector": "<andriod resource-id='com.android.contacts:id/data'/>", "method": "gettext", "args": {}, "attrs": {}}
.//node[@resource-id="com.android.contacts:id/data"]
performing gettext
Bart'Phone Number is 188 8888 8888
```

