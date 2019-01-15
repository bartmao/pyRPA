# pyRPA
A slim RPA framework automated by Python, can integrated with other RPA tools, like UIPath. Currently only support UIPath(RPA.UIPathAdapter). 
The main idea I use python to do RPA because:
1. Pure code is more easy to maintain auto-generated code by the RPA designers
2. Can easily do the interception things

## Setup
Using UIPath
1. Checkout file [pyRPA/RPA.UIPathAdapter/binary/RPA.UIPathAdapter.exe.config], update `UIPathActFolder` to your own uipath folder
2. Run adapter pyRPA/RPA.UIPathAdapter/binary/RPA.UIPathAdapter.exe under administrator permission
3. Add host entry '127.0.0.1 Bart'

## Sample 1 (pyRPA/sample.py)

This sample will automatically open notepad, type something and close it. 
1. It will create logs before and after each UI automation
2. It will highlight the element to be operated

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
