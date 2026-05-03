$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot

Write-Host "Stopping mysql + redis..." -ForegroundColor Cyan
docker compose -f (Join-Path $root "docker-compose.yml") stop mysql redis

Write-Host "Done." -ForegroundColor Green
Write-Host "Backend / frontend / natapp windows can be closed directly."
