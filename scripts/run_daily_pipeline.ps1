# World Cup Market Intelligence — Daily Pipeline Runner
# Rulează automat: snapshot Polymarket + trends workflow + daily brief
# Destinat Windows Task Scheduler, zilnic la 08:00
#
# Powered by Mayior Capital.

param(
    [string]$ProjectRoot = $PSScriptRoot | Split-Path -Parent,
    [switch]$SkipPolymarket,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logFile = Join-Path $ProjectRoot "logs\daily_pipeline.log"

# Asigură că folderul logs există
New-Item -ItemType Directory -Force -Path (Join-Path $ProjectRoot "logs") | Out-Null

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $line = "[$timestamp] [$Level] $Message"
    Write-Host $line
    Add-Content -Path $logFile -Value $line -Encoding UTF8
}

function Run-Step {
    param([string]$Name, [string]$Command, [string]$WorkDir)
    Write-Log "START: $Name"
    Push-Location $WorkDir
    try {
        Invoke-Expression $Command
        if ($LASTEXITCODE -ne 0) {
            Write-Log "FAIL: $Name (exit code $LASTEXITCODE)" "ERROR"
            return $false
        }
        Write-Log "PASS: $Name"
        return $true
    } catch {
        Write-Log "FAIL: $Name — $_" "ERROR"
        return $false
    } finally {
        Pop-Location
    }
}

# ── Detectează Python (venv sau system) ───────────────────────────────────────
$venvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$python = if (Test-Path $venvPython) { $venvPython } else { "python" }

Write-Log "=== World Cup Market Intelligence — Daily Pipeline ==="
Write-Log "Project root: $ProjectRoot"
Write-Log "Python: $python"
Write-Log "Log file: $logFile"

Set-Location $ProjectRoot

# ── Step 1: Validare proiect ──────────────────────────────────────────────────
$ok = Run-Step "Project validation" "$python scripts\validate_project.py" $ProjectRoot
if (-not $ok) {
    Write-Log "Pipeline aborted: validation failed." "ERROR"
    exit 1
}

# ── Step 2: Snapshot Polymarket (live) ────────────────────────────────────────
if (-not $SkipPolymarket) {
    $ok = Run-Step "Polymarket snapshot" "$python scripts\update_snapshot.py --provider polymarket" $ProjectRoot
    if (-not $ok) {
        Write-Log "Polymarket snapshot failed — continuăm cu datele existente." "WARN"
    }

    Run-Step "Polymarket YES ranking" "$python scripts\generate_polymarket_yes_ranking.py" $ProjectRoot | Out-Null
}

# ── Step 3: Trends workflow (compară snapshot-uri) ────────────────────────────
Run-Step "Historical trends workflow" "$python scripts\run_historical_trends_workflow.py --provider polymarket" $ProjectRoot | Out-Null

# ── Step 4: Dashboard metadata ────────────────────────────────────────────────
Run-Step "Dashboard metadata" "$python scripts\generate_dashboard_metadata.py" $ProjectRoot | Out-Null

# ── Step 5: Trends dashboard ──────────────────────────────────────────────────
Run-Step "Trends dashboard" "$python scripts\generate_trends_dashboard.py" $ProjectRoot | Out-Null

# ── Step 6: Daily brief ───────────────────────────────────────────────────────
$ok = Run-Step "Daily brief" "$python scripts\generate_daily_brief.py" $ProjectRoot
if (-not $ok) {
    Write-Log "Daily brief generation failed." "ERROR"
    exit 1
}

# ── Step 7: Operator performance (privat, nu se commitează) ───────────────────
$perfScript = Join-Path $ProjectRoot "scripts\analyze_operator_performance.py"
if (Test-Path $perfScript) {
    Run-Step "Operator performance" "$python scripts\analyze_operator_performance.py" $ProjectRoot | Out-Null
}

# ── Step 8: Git commit automat ────────────────────────────────────────────────
Write-Log "Committing public outputs to git..."
Set-Location $ProjectRoot

git add docs\briefs\ docs\trends-dashboard\index.html docs\polymarket-dashboard\index.html 2>&1 | Out-Null

$gitStatus = git status --porcelain 2>&1
if ($gitStatus) {
    $commitMsg = "Daily pipeline: $(Get-Date -Format 'yyyy-MM-dd HH:mm') UTC"
    git commit -m $commitMsg 2>&1 | Write-Log
    git push 2>&1 | Write-Log
    Write-Log "Committed and pushed: $commitMsg"
} else {
    Write-Log "Nothing to commit — no changes in public outputs."
}

Write-Log "=== Daily pipeline complete ==="
Write-Log "Daily brief: docs\briefs\$(Get-Date -Format 'yyyy-MM-dd').md"
