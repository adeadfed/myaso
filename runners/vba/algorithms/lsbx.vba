Private Function GetLSBX(ByVal Target As Byte, ByVal Source As Byte) As Byte
    GetLSBX = (Target * 2) Or (Source And 1)
End Function

Private Function Read(Bmp As BITMAP, lPayloadSize As Long, bChannel As Byte) As Byte()
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
            
            
            lBytePos = Int(lBitPos / 8)
            If lBitLength <= 0 Then
                bPayloadArr(lBytePos) = 0
                
                Read = bPayloadArr
                Exit Function
            End If
            
            bPayloadArr(lBytePos) = GetLSBX(bPayloadArr(lBytePos), bChannelsArr(bChannel))
            lBitPos = lBitPos + 1
            lBitLength = lBitLength - 1
            
        Next x
        lYOffset = lYOffset - lRowLength
    Next y
End Function