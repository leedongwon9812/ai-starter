# wifi-reconnect.ps1

Write-Host "1. Disconnecting Wi-Fi..."
Disable-NetAdapter -Name "Wi-Fi" -Confirm:$false

Write-Host "2. Waiting 10 seconds..."
Start-Sleep -Seconds 10

Write-Host "3. Connecting Wi-Fi..."
Enable-NetAdapter -Name "Wi-Fi" -Confirm:$false

Write-Host "4. Waiting for connection..."
Start-Sleep -Seconds 5

Write-Host "5. Checking network..."

if (Test-Connection -ComputerName "8.8.8.8" -Count 1 -Quiet) {
    Write-Host "SUCCESS: Network is connected."
}
else {
    Write-Host "FAIL: Network connection failed."
}