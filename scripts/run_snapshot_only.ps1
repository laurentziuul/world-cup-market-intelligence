# World Cup Market Intelligence - Intraday Snapshot Runner
# Collects a Polymarket snapshot without generating briefs, committing, or pushing.
# Run this script for intraday cadence (e.g. 18:00, 21:30, 00:30 Romania local time).
# Full daily pipeline with brief generation runs separately at 08:00.
#
# Usage:
#   .\scripts\run_snapshot_only.ps1
#
# The snapshot is saved to:
#   data/processed/snapshots/{timestamp}-polymarket.csv
#
# Logs are written to:
#   logs\snapshot_only.log
#
# This script does NOT commit, push, or touch data/private/.
#
# Powered by Mayior Capital.

param(
    [string]$ProjectRoot = "",
    [switch]$Verbose
)

# Detect ProjectRoot from script location
if (-not $ProjectRoot) {
    $scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
    $ProjectRoot = Split-Path -Parent $scriptDir
}

# Hardcoded fallback if detection fails
if (-not $ProjectRoot -or -not (Test-Path $ProjectRoot)) {
    $ProjectRoot = "C:\Users\laure\projects\world-cup-market-intelligence-v0"
}

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logFile = Join-Path $ProjectRoot "logs\snapshot_only.log"

# Ensure logs folder exists
New-Item -ItemType Directory -Force -Path (Join-Path $ProjectRoot "logs") | Out-Null

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $line = "[$timestamp] [$Level] $Message"
    Write-Host $line
    Add-Content -Path $logFile -Value $line -Encoding UTF8
}

# Detect Python (venv preferred, required)
$venvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Log "ERROR: .venv Python not found at: $venvPython" "ERROR"
    Write-Log "Run: python -m venv .venv && .venv\Scripts\pip install -e ." "ERROR"
    exit 1
}

$python = $venvPython

Write-Log "=== Intraday Snapshot Runner ==="
Write-Log "Project root: $ProjectRoot"
Write-Log "Python: $python"
Write-Log "Log file: $logFile"

Set-Location $ProjectRoot

# Run snapshot only
Write-Log "START: Polymarket snapshot"

try {
    & $python scripts\update_snapshot.py --provider polymarket
    $exitCode = $LASTEXITCODE
} catch {
    Write-Log "FAIL: Polymarket snapshot - $_" "ERROR"
    exit 1
}

if ($exitCode -ne 0) {
    Write-Log "FAIL: Polymarket snapshot exited with code $exitCode" "ERROR"
    exit $exitCode
}

Write-Log "PASS: Polymarket snapshot complete"
Write-Log "Snapshot saved to: data\processed\snapshots\"
Write-Log "=== Snapshot runner complete. No commit. No push. ==="
