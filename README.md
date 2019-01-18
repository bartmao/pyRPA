# pyRPA
A slim RPA framework automated by Python, can integrated with other RPA tools, like UIPath. Currently support
1. UIPath(RPA.UIPathAdapter)
2. Andriod Platform(android/droidagent.py)

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
2. Install android SDK(optional, we can use it to inspect elements)

## Sample 1 (pyRPA/sample.py)

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

## Sample 2 (pyRPA/sample-andriod.py)
This sample will search specific contact and print the phone number for you
