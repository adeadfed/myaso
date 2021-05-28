function get_lsbm([byte]$target, [byte]$source) {
    $a = $target -shl 1
    $b = $source % 2
    $a -bor $b
}

function get_payload($BitMap, $length) {
    [Int32]$pos = 0
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
                $bytes[$idx] = get_lsbm $bytes[$idx] $byte

                $pos += 1
                $length -= 1
            }
        }
    }
}
