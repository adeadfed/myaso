[string] $filename = ".\samples\helpme.bmp"
[Int32] $length = 128 + 1
$BitMap = [System.Drawing.Image]::FromFile((Get-Item $filename).fullname, $true)

$bits = New-Object System.Collections.BitArray($length)

[Int32]$pos = 0

function ConvertToBytes([System.Collections.Bitarray]$bits) {
    $ret = new-object byte[] ([int][Math]::Floor(($bits.Length - 1) / 8) + 1)
    $bits.CopyTo($ret, 0)
    $ret
}

$signature = @"
[DllImport("Crypt32.dll", CharSet = CharSet.Auto, SetLastError = true)]
public static extern bool CryptStringToBinary(
    string pszString,
    int cchString,
    int dwFlags,
    byte[] pbBinary,
    ref int pcbBinary,
    int pdwSkip,
    ref int pdwFlags
);
[DllImport("Crypt32.dll", CharSet = CharSet.Auto, SetLastError = true)]
public static extern bool CryptBinaryToString(
    byte[] pbBinary,
    int cbBinary,
    int dwFlags,
    StringBuilder pszString,
    ref int pcchString
);
"@

foreach($y in (($BitMap.Height-1)..0)) {
	foreach($x in (0..($BitMap.Width-1))) {
		$Pixel = $BitMap.GetPixel($x,$y)
        $B = $Pixel | Select-Object -ExpandProperty B
        $G = $Pixel | Select-Object -ExpandProperty G
        $R = $Pixel | Select-Object -ExpandProperty R

        # "($B, $G, $R)"
        
        foreach ($bit in ($Pixel.B, $Pixel.G, $Pixel.R)) {
            if ($length -le 0) { 
                foreach ($bit in $bits) { $b = [int]$bit; Write-Host -NoNewline $b }
                ConvertToBytes($bits)
                exit
            }
            # $bit
            $b = [int]([byte]$bit -band 0x01)
            $bits.Set($pos, $b)
            $pos += 1
            $length -= 1
        }
    }
}
