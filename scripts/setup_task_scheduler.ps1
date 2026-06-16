# World Cup Market Intelligence — Windows Task Scheduler Setup
# Înregistrează automat task-ul zilnic în Windows Task Scheduler
#
# Rulează o singură dată ca Administrator:
#   Right-click PowerShell → "Run as Administrator"
#   cd C:\Users\laure\projects\world-cup-market-intelligence-v0
#   .\scripts\setup_task_scheduler.ps1
#
# Powered by Mayior Capital.

param(
    [string]$TaskName = "WorldCupMarketIntelligence-DailyPipeline",
    [string]$RunAtHour = "8",   # 08:00 dimineata
    [string]$RunAtMinute = "0",
    [switch]$Remove
)

$ProjectRoot = $PSScriptRoot | Split-Path -Parent
$scriptPath  = Join-Path $ProjectRoot "scripts\run_daily_pipeline.ps1"
$logDir      = Join-Path $ProjectRoot "logs"

# ── Remove task ───────────────────────────────────────────────────────────────
if ($Remove) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "Task '$TaskName' removed."
    exit 0
}

# ── Verificări ────────────────────────────────────────────────────────────────
if (-not (Test-Path $scriptPath)) {
    Write-Error "Nu găsesc scriptul: $scriptPath"
    exit 1
}

New-Item -ItemType Directory -Force -Path $logDir | Out-Null

# ── Detectează Python ─────────────────────────────────────────────────────────
$venvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$python = if (Test-Path $venvPython) { $venvPython } else { (Get-Command python).Source }

Write-Host "Python detectat: $python"
Write-Host "Script: $scriptPath"
Write-Host "Ora de rulare: $RunAtHour`:$($RunAtMinute.PadLeft(2,'0'))"

# ── Creează action: rulează PowerShell cu scriptul ────────────────────────────
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`" -ProjectRoot `"$ProjectRoot`"" `
    -WorkingDirectory $ProjectRoot

# ── Trigger: zilnic la ora setată ─────────────────────────────────────────────
$trigger = New-ScheduledTaskTrigger `
    -Daily `
    -At "$($RunAtHour.PadLeft(2,'0')):$($RunAtMinute.PadLeft(2,'0'))"

# ── Settings ──────────────────────────────────────────────────────────────────
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 30) `
    -StartWhenAvailable `
    -WakeToRun:$false `
    -RunOnlyIfNetworkAvailable

# ── Principal: rulează ca userul curent ───────────────────────────────────────
$principal = New-ScheduledTaskPrincipal `
    -UserId ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name) `
    -LogonType Interactive `
    -RunLevel Highest

# ── Înregistrare task ─────────────────────────────────────────────────────────
$existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existing) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Task existent șters, se recreează..."
}

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "World Cup Market Intelligence — Daily Polymarket snapshot + brief @ Mayior Capital" | Out-Null

Write-Host ""
Write-Host "✓ Task creat cu succes: $TaskName"
Write-Host "  Rulează zilnic la: $($RunAtHour.PadLeft(2,'0')):$($RunAtMinute.PadLeft(2,'0'))"
Write-Host "  Log-uri: $logDir\daily_pipeline.log"
Write-Host ""
Write-Host "Comenzi utile:"
Write-Host "  # Verifică task-ul:"
Write-Host "  Get-ScheduledTask -TaskName '$TaskName'"
Write-Host ""
Write-Host "  # Rulează acum manual:"
Write-Host "  Start-ScheduledTask -TaskName '$TaskName'"
Write-Host ""
Write-Host "  # Șterge task-ul:"
Write-Host "  .\scripts\setup_task_scheduler.ps1 -Remove"
Write-Host ""
Write-Host "  # Schimbă ora (ex: 07:30):"
Write-Host "  .\scripts\setup_task_scheduler.ps1 -RunAtHour 7 -RunAtMinute 30"
