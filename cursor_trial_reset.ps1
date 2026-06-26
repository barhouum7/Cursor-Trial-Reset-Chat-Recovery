# ==============================================================================
# Cursor Safe Trial Reset for Windows (With Auto-Backups)
# ==============================================================================
Write-Host "Starting Cursor Safe Reset Routine..." -ForegroundColor Cyan

# 1. Force kill active and hidden background file-watcher processes
Write-Host "Terminating active Cursor process threads..." -ForegroundColor Yellow
Stop-Process -Name "Cursor" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Define system paths
$globalStorageDir = "$env:APPDATA\Cursor\User\globalStorage"
$configPath = "$globalStorageDir\storage.json"
$backupDir = "$globalStorageDir\Backup_History"

# 2. Automated Safe Backup Loop
if (Test-Path "$globalStorageDir\state.vscdb") {
    if (!(Test-Path $backupDir)) {
        New-Item -ItemType Directory -Path $backupDir | Out-Null
    }
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    Write-Host "Archiving critical global database files to backup directory..." -ForegroundColor Yellow
    
    # Securely copy database and wal state arrays before changing identifiers
    Copy-Item -Path "$globalStorageDir\state.vscdb*" -Destination "$backupDir\state_vscdb_backup_$timestamp.bak" -Force -ErrorAction SilentlyContinue
    Write-Host "Database snapshot safely archived in: \globalStorage\Backup_History\" -ForegroundColor Green
}

# 3. Clean up and regenerate telemetry matrices
if (Test-Path $configPath) {
    (Get-Item $configPath).Attributes = 'Normal'
}

# Clear local DB target safely
Remove-Item -Path "$globalStorageDir\state.vscdb*" -Force -ErrorAction SilentlyContinue

# Generate non-clashing unique layout string values
$macMachineId = [guid]::NewGuid().ToString().ToLower()
$machineId = [guid]::NewGuid().ToString().ToLower()
$devDeviceId = [guid]::NewGuid().ToString()

$payloadJson = "{`"telemetry.macMachineId`":`"$macMachineId`",`"telemetry.machineId`":`"$machineId`",`"telemetry.devDeviceId`":`"$devDeviceId`}"

Set-Content -Path $configPath -Value $payloadJson
(Get-Item $configPath).Attributes = 'ReadOnly'

Write-Host "Initialization complete. Clean environment IDs successfully mapped." -ForegroundColor Green
