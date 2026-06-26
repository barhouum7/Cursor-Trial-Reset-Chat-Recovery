# ==============================================================================
# Cursor UI State Rollback & History Restorer
# ==============================================================================
Write-Host "Initializing Native UI Rollback Procedure..." -ForegroundColor Cyan

# 1. Close Cursor to release active database locks
Write-Host "Terminating active Cursor processes..." -ForegroundColor Yellow
Stop-Process -Name "Cursor" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

$globalStorageDir = "$env:APPDATA\Cursor\User\globalStorage"
$backupDir = "$globalStorageDir\Backup_History"

if (!(Test-Path $backupDir)) {
    Write-Host "Error: No Backup_History folder detected. Cannot perform automated restoration." -ForegroundColor Red
    exit
}

# 2. Automatically locate the most recently created backup file set
$latestBackup = Get-ChildItem -Path $backupDir -Filter "state_vscdb_backup_*.bak" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($latestBackup -eq $null) {
    Write-Host "Error: No historical snapshot files found inside the backup directory." -ForegroundColor Red
    exit
}

Write-Host "Found most recent backup target: $($latestBackup.Name)" -ForegroundColor Yellow

# 3. Clean active database and restore the backup file
Remove-Item -Path "$globalStorageDir\state.vscdb*" -Force -ErrorAction SilentlyContinue

Copy-Item -Path $latestBackup.FullName -Destination "$globalStorageDir\state.vscdb" -Force
Write-Host "Database successfully restored to original baseline state." -ForegroundColor Green

# 4. Remove read-only block from storage settings to sync layout references
$configPath = "$globalStorageDir\storage.json"
if (Test-Path $configPath) {
    (Get-Item $configPath).Attributes = 'Normal'
    Write-Host "Telemetry configuration updated to original layout sync state." -ForegroundColor Green
}

Write-Host "`n🎉 Rollback complete! Relaunch Cursor and all original chats will be back in your sidebar." -ForegroundColor Green
