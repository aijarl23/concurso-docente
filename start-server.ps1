$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root "venv\Scripts\python.exe"
$port = if ($env:PORT) { [int]$env:PORT } else { 8001 }

if (-not (Test-Path $python)) {
    Write-Host "No se encontro el entorno virtual en: $python" -ForegroundColor Red
    exit 1
}

Set-Location $root

$existing = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
if ($existing) {
    foreach ($conn in $existing) {
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$($conn.OwningProcess)" -ErrorAction SilentlyContinue
        if ($proc -and $proc.CommandLine -like "*ConcursoDocente*manage.py*runserver*") {
            Stop-Process -Id $conn.OwningProcess -Force
        } else {
            Write-Host "El puerto $port esta ocupado por otro proceso:" -ForegroundColor Yellow
            Write-Host $proc.CommandLine
            exit 1
        }
    }
    Start-Sleep -Seconds 1
}

Write-Host "Iniciando ConcursoDocente en http://127.0.0.1:$port/" -ForegroundColor Green
& $python manage.py runserver "127.0.0.1:$port"
