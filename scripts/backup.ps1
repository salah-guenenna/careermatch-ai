param([string]$OutputDirectory = ".\backups")
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$dump = Join-Path $OutputDirectory "careermatch-$stamp.sql"
$uploads = Join-Path $OutputDirectory "uploads-$stamp.zip"
docker compose exec -T db pg_dump -U careermatch -d careermatch | Out-File -Encoding utf8 $dump
if (Test-Path -LiteralPath ".\uploads") { Compress-Archive -Path .\uploads\* -DestinationPath $uploads -Force }
Write-Output "Database backup: $dump"
Write-Output "Uploads backup: $uploads"

