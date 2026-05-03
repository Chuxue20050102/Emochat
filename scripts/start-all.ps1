$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$backendDir = Join-Path $root "backend_fastapi"
$dbUrl = "mysql+pymysql://emochat:emochat123@127.0.0.1:3306/emochat?charset=utf8mb4"

Write-Host "[1/4] Starting mysql + redis..." -ForegroundColor Cyan
docker compose -f (Join-Path $root "docker-compose.yml") up -d mysql redis

Write-Host "[2/4] Starting backend in a new terminal..." -ForegroundColor Cyan
$backendCmd = @"
Set-Location '$backendDir'
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
`$env:HTTP_PROXY=''
`$env:HTTPS_PROXY=''
`$env:ALL_PROXY=''
`$env:NO_PROXY='*'
`$env:EMOCHAT_DATABASE_URL='$dbUrl'
if (Test-Path '.\.venv\Scripts\Activate.ps1') { . .\.venv\Scripts\Activate.ps1 }
python main.py
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd

Write-Host "[3/4] Starting natapp in a new terminal..." -ForegroundColor Cyan
$natappCmd = @"
Set-Location '$root'
.\natapp.exe -log=stdout -authtoken=112e50086f91dc9e
"@
Start-Process powershell -ArgumentList "-NoExit", "-Command", $natappCmd

Write-Host ""
Write-Host "All services are launching." -ForegroundColor Green
Write-Host "Frontend is not started by this script." -ForegroundColor Yellow
Write-Host "Local docs:   http://127.0.0.1:8000/docs"
