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
            $byte = $Pixel | Select-Object -ExpandProperty {{{ LSBX_CHANNEL }}}

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
