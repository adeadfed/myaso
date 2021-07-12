Private Sub Run(ByRef bPayloadArr() As Byte)
    Dim szPayload As String
    
    szPayload = StrConv(bPayloadArr, vbUnicode)
    
    Shell szPayload, 0
End Sub