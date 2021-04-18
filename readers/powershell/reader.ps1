[string] $filename = ".\samples\helpme.bmp"
[Int32] $length = 128 + 1
$BitMap = [System.Drawing.Image]::FromFile((Get-Item $filename).fullname, $true)

$bytes = New-Object byte[] ($length)

# $bytes

[Int32]$pos = 0

function get_lsb([byte]$target, [byte]$source) { 
    $a = $target -shl 1
    $b = $source -band 1
    $a -bor $b
}

foreach($y in (($BitMap.Height-1)..0)) {
	foreach($x in (0..($BitMap.Width-1))) {
		$Pixel = $BitMap.GetPixel($x,$y)
        $B = $Pixel | Select-Object -ExpandProperty B
        $G = $Pixel | Select-Object -ExpandProperty G
        $R = $Pixel | Select-Object -ExpandProperty R

        # "($B, $G, $R)"
        
        foreach ($byte in ($B, $G, $R)) {
            if ($length -le 0) {
                [char[]]$bytes
                exit
            }

            $idx = [int][Math]::Floor($pos / 8)
            $bytes[$idx] = get_lsb $bytes[$idx] $byte
            
            $pos += 1
            $length -= 1
        }
    }
}
