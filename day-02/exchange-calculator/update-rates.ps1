$ErrorActionPreference = 'Stop'
$folder = Join-Path $PSScriptRoot ''
New-Item -ItemType Directory -Force -Path $folder | Out-Null
$url = 'https://api.frankfurter.dev/v1/latest?from=USD&to=KRW,JPY,EUR'
$data = Invoke-RestMethod -Uri $url -TimeoutSec 30
if ($data.base -ne 'USD' -or $data.amount -ne 1 -or $data.date -notmatch '^\d{4}-\d{2}-\d{2}$') { throw 'Invalid API response' }
$rows = foreach ($currency in @('KRW', 'JPY', 'EUR')) {
    $rate = [double]$data.rates.$currency
    if ($rate -le 0 -or [double]::IsInfinity($rate) -or [double]::IsNaN($rate)) { throw "Invalid rate: $currency" }
    '{0},USD,{1},{2}' -f $data.date,$currency,$rate.ToString('R',[Globalization.CultureInfo]::InvariantCulture)
}
$csvPath = Join-Path $folder 'exchange-rates.csv'
$csv = "date,base,currency,rate`n" + ($rows -join "`n") + "`n"
# Keep every successful collection for future time-series charts.
# date is the provider's rate date; collected_at is the actual collection time.
$collectedAt = [DateTimeOffset]::Now.ToString('yyyy-MM-ddTHH:mm:sszzz')
$historyPath = Join-Path $folder 'exchange-rate-history.csv'
$historyHeader = 'date,base,currency,rate,collected_at'
if (Test-Path -LiteralPath $historyPath) {
    $header = Get-Content -LiteralPath $historyPath -TotalCount 1
    if ($header -ne $historyHeader) { throw 'Unexpected history CSV columns; existing history was preserved.' }
} else {
    [IO.File]::WriteAllText($historyPath, "$historyHeader`n", [Text.UTF8Encoding]::new($false))
}
$historyRows = ($rows | ForEach-Object { "$_,$collectedAt" }) -join "`n"
[IO.File]::AppendAllText($historyPath, "$historyRows`n", [Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText($csvPath,$csv,[Text.UTF8Encoding]::new($false))
# Read the saved CSV back. This copy allows double-click use without a web server.
$savedCsv = [IO.File]::ReadAllText($csvPath)
$script = 'window.savedCsv = ' + (ConvertTo-Json -InputObject $savedCsv -Compress) + ';'
[IO.File]::WriteAllText((Join-Path $folder 'rates-data.js'),$script,[Text.UTF8Encoding]::new($false))
Write-Host "Saved: $csvPath (date: $($data.date))"
