from pyOpenRPA.Tools import CrossOS
if CrossOS.IS_WINDOWS_BOOL: import win32clipboard #CrossOS
if CrossOS.IS_LINUX_BOOL: import pyclip #CrossOS
import keyboard # keyboard functions
import time # Some operations need wait
import secrets
gWaitTextInClipboardSec = 1 # Second for wait text will be set in clipboard (for get operations)
# set clipboard data
def TextSet(inTextStr):
    if CrossOS.IS_WINDOWS_BOOL:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(inTextStr)
        win32clipboard.CloseClipboard()
    if CrossOS.IS_LINUX_BOOL:
        pyclip.copy(inTextStr) # copy data to the clipboard
# get clipboard data
def TextGet(inWaitTextInClipboardSec = gWaitTextInClipboardSec):
    time.sleep(inWaitTextInClipboardSec) # Wait for clipboard will save
    if CrossOS.IS_WINDOWS_BOOL:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data
    if CrossOS.IS_LINUX_BOOL:
        lResult = pyclip.paste(text=True)
        return lResult
# Test in has text cursor and ready to apply
def InputIsFocused():
    keyboard.press_and_release("ctrl+a")
    keyboard.press_and_release("backspace") # remove old text
    lTextForTest = str(secrets.randbelow(99899)+100)
    keyboard.write(lTextForTest)
    keyboard.press_and_release("ctrl+a")
    keyboard.press_and_release("ctrl+c")
    time.sleep(2)
    keyboard.press_and_release("backspace")  # remove old text
    lClipboardText = TextGet()
    lResult = lClipboardText == lTextForTest
    return lResult
# Check if cmd is opened
def CMDIsOpen():
    lTextForTest = str(secrets.randbelow(99899)+100)
    keyboard.write(lTextForTest+" |clip")
    keyboard.press_and_release("enter")
    time.sleep(2)
    lClipboardText = TextGet()
    lResult = lClipboardText == lTextForTest
    return lResult