#Include include.ahk

args = %1%
path := DefaultBrowser()

Run, %path% %args%