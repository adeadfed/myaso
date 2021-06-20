Private Declare Function IsClipboardFormatAvailable Lib "user32" (ByVal wFormat As Integer) As Long

Private Declare Function OpenClipboard Lib "user32" (ByVal hwnd As Long) As Long
Private Declare Function CloseClipboard Lib "user32" () As Long

Private Declare Function GetClipboardData Lib "user32" (ByVal wFormat As Integer) As Long

Private Declare Function CopyImage Lib "user32" (ByVal handle As Long, ByVal un1 As Long, ByVal n1 As Long, ByVal n2 As Long, ByVal un2 As Long) As Long
Private Declare Function GetObjectA Lib "Gdi32" (ByVal handle As Long, ByVal c As Long, ByRef pv As BITMAP86) As Long

Private Type BITMAP
    bmType As Long
    bmWidth As Long
    bmHeight As Long
    bmWidthBytes As Long
    bmPlanes As Integer
    bmBitsPixel As Integer
    bmBits As Long
End Type