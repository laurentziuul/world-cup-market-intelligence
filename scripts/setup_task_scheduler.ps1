# World Cup Market Intelligence - Windows Task Scheduler Setup
# Registers the daily pipeline task in Windows Task Scheduler
#
# Run once as Administrator:
#   Right-click PowerShell -> "Run as Administrator"
#   cd C:\Users\laure\projects\world-cup-market-intelligence-v0
#   .\scripts\setup_task_scheduler.ps1
#
# Powered by Mayior Capital.

param(
    [string]$TaskName = "WorldCupMarketIntelligence-DailyPipeline",
    [string]$RunAtHour = "8",
    [string]$RunAtMinute = "0",
    [switch]$Remove
)

$ProjectRoot = $PSScriptRoot | Split-Path -Parent
$scriptPath  = Join-Path $ProjectRoot "scripts\run_daily_pipeline.ps1"
$logDir      = Join-Path $ProjectRoot "logs"

# Remove task
if ($Remove) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Task '$TaskName' removed."
    exit 0
}

# Checks
if (-not (Test-Path $scriptPath)) {
    Write-Error "Script not found: $scriptPath"
    exit 1
}

New-Item -ItemType Directory -Force -Path $logDir | Out-Null

# Detect Python
$venvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$python = if (Test-Path $venvPython) { $venvPython } else { (Get-Command python).Source }

Write-Host "Python detected: $python"
Write-Host "Script: $scriptPath"
Write-Host "Scheduled time: $($RunAtHour.PadLeft(2,'0')):$($RunAtMinute.PadLeft(2,'0'))"

# Create action
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`" -ProjectRoot `"$ProjectRoot`"" `
    -WorkingDirectory $ProjectRoot

# Trigger: daily at set time
$trigger = New-ScheduledTaskTrigger `
    -Daily `
    -At "$($RunAtHour.PadLeft(2,'0')):$($RunAtMinute.PadLeft(2,'0'))"

# Settings
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
    -StartWhenAvailable `
    -WakeToRun:$false `
    -RunOnlyIfNetworkAvailable

# Principal: run as current user
$principal = New-ScheduledTaskPrincipal `
    -UserId ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name) `
    -LogonType Interactive `
    -RunLevel Highest

# Remove existing task if present
$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Existing task removed, recreating..."
}

# Register task
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "World Cup Market Intelligence - Daily Polymarket snapshot + brief @ Mayior Capital" | Out-Null

Write-Host ""
Write-Host "Task created successfully: $TaskName"
Write-Host "Runs daily at: $($RunAtHour.PadLeft(2,'0')):$($RunAtMinute.PadLeft(2,'0'))"
Write-Host "Log file: $logDir\daily_pipeline.log"
Write-Host ""
Write-Host "Useful commands:"
Write-Host "  # Check task status:"
Write-Host "  Get-ScheduledTask -TaskName '$TaskName'"
Write-Host ""
Write-Host "  # Run now manually:"
Write-Host "  Start-ScheduledTask -TaskName '$TaskName'"
Write-Host ""
Write-Host "  # Remove task:"
Write-Host "  .\scripts\setup_task_scheduler.ps1 -Remove"
Write-Host ""
Write-Host "  # Change time (e.g. 07:30):"
Write-Host "  .\scripts\setup_task_scheduler.ps1 -RunAtHour 7 -RunAtMinute 30"
