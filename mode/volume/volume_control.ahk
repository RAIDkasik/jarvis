#if (GetKeyState("Rbutton", "P"))
{
WheelUp::
Send {Volume_Up}
Return

WheelDown::
Send {Volume_Down}
Return
}