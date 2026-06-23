# World Cup Market Intelligence - Daily Pipeline Runner
# Runs automatically: Polymarket snapshot + trends workflow + daily brief
# Designed for Windows Task Scheduler, daily at 08:00
#
# Powered by Mayior Capital.

param(
    [string]$ProjectRoot = "",
    [switch]$SkipPolymarket,
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
$logFile = Join-Path $ProjectRoot "logs\daily_pipeline.log"

# Ensure logs folder exists
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
        Write-Log "FAIL: $Name - $_" "ERROR"
        return $false
    } finally {
        Pop-Location
    }
}

# Detect Python (venv or system)
$venvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$python = if (Test-Path $venvPython) { $venvPython } else { "python" }

Write-Log "=== World Cup Market Intelligence - Daily Pipeline ==="
Write-Log "Project root: $ProjectRoot"
Write-Log "Python: $python"
Write-Log "Log file: $logFile"

Set-Location $ProjectRoot

# Step 1: Project validation
$ok = Run-Step "Project validation" "$python scripts\validate_project.py" $ProjectRoot
if (-not $ok) {
    Write-Log "Pipeline aborted: validation failed." "ERROR"
    exit 1
}

# Step 2: Polymarket snapshot (live)
if (-not $SkipPolymarket) {
    $ok = Run-Step "Polymarket snapshot" "$python scripts\update_snapshot.py --provider polymarket" $ProjectRoot
    if (-not $ok) {
        Write-Log "Polymarket snapshot failed - continuing with existing data." "WARN"
    }

    Run-Step "Polymarket YES ranking" "$python scripts\generate_polymarket_yes_ranking.py" $ProjectRoot | Out-Null
}

# Step 3: Trends workflow (compare snapshots)
Run-Step "Historical trends workflow" "$python scripts\run_historical_trends_workflow.py --provider polymarket" $ProjectRoot | Out-Null

# Step 4: Dashboard metadata
Run-Step "Dashboard metadata" "$python scripts\generate_dashboard_metadata.py" $ProjectRoot | Out-Null

# Step 5: Trends dashboard
Run-Step "Trends dashboard" "$python scripts\generate_trends_dashboard.py" $ProjectRoot | Out-Null

# Step 5b: Polymarket live dashboard (reads from ranking CSV produced in Step 2 - no extra API call)
Run-Step "Polymarket live dashboard" "$python scripts\generate_polymarket_live_dashboard.py" $ProjectRoot | Out-Null

# Step 6a: Snapshot plan (must run before daily brief)
Run-Step "Snapshot plan" "$python scripts\generate_snapshot_plan.py" $ProjectRoot | Out-Null

# Step 6b: Daily brief
$ok = Run-Step "Daily brief" "$python scripts\generate_daily_brief.py" $ProjectRoot
if (-not $ok) {
    Write-Log "Daily brief generation failed." "ERROR"
    exit 1
}

# Step 7: Operator performance (private, not committed)
$perfScript = Join-Path $ProjectRoot "scripts\analyze_operator_performance.py"
if (Test-Path $perfScript) {
    Run-Step "Operator performance" "$python scripts\analyze_operator_performance.py" $ProjectRoot | Out-Null
}

# Helper: run a git command with ErrorActionPreference = Continue so that
# git stderr warnings (e.g. LF/CRLF notices) do not throw NativeCommandError.
# Returns the captured output lines. Sets script-scope $script:gitCode.
function Invoke-Git {
    param([string[]]$GitArgs)
    $old = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $out = & git @GitArgs 2>&1
        $script:gitCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $old
    }
    return $out
}

# Step 8: Git auto-commit public outputs only
Write-Log "Committing public outputs to git..."
Set-Location $ProjectRoot

# Public output paths to stage - never use git add .
$gitAddPaths = @(
    "docs\briefs\",
    "docs\trends-dashboard\index.html",
    "docs\polymarket-dashboard\index.html"
)

$stagedPaths = @()

foreach ($addPath in $gitAddPaths) {
    $fullAddPath = Join-Path $ProjectRoot $addPath

    if (-not (Test-Path $fullAddPath)) {
        Write-Log "SKIP missing output: $addPath"
        continue
    }

    # Check if path is gitignored before attempting git add.
    # git check-ignore exits 0 = ignored, non-zero = not ignored.
    $null = Invoke-Git @("check-ignore", "-q", "--", $fullAddPath)
    if ($script:gitCode -eq 0) {
        Write-Log "SKIP ignored output: $addPath"
        continue
    }

    # Attempt git add -- <path>; warnings logged, only non-zero exit is failure.
    $addOut = Invoke-Git @("add", "--", $fullAddPath)
    if ($addOut) { $addOut | ForEach-Object { Write-Log "$_" } }
    if ($script:gitCode -ne 0) {
        Write-Log "git add FAILED for '$addPath' (exit $($script:gitCode))" "ERROR"
        if ($stagedPaths.Count -gt 0) {
            Invoke-Git @("reset", "HEAD", "--") + $stagedPaths | Out-Null
        }
        Write-Log "Pipeline aborted: git add failed for '$addPath'." "ERROR"
        exit 1
    }
    $stagedPaths += $fullAddPath
}

# Check only what we staged, not all working tree changes.
$stagedOut = Invoke-Git @("diff", "--cached", "--name-only")
$gitStaged = $stagedOut | Where-Object { $_ -and $_.Trim() -ne "" }
if ($gitStaged) {
    Write-Log "Staged files: $($gitStaged -join ', ')"
    $commitMsg = "Daily pipeline: $(Get-Date -Format 'yyyy-MM-dd HH:mm') UTC"

    $commitOut = Invoke-Git @("commit", "-m", $commitMsg)
    $commitCode = $script:gitCode
    if ($commitOut) { Write-Log "git commit: $($commitOut -join ' | ')" }

    if ($commitCode -ne 0) {
        Write-Log "git commit failed (exit $commitCode) - resetting staged files." "WARN"
        if ($stagedPaths.Count -gt 0) {
            Invoke-Git (@("reset", "HEAD", "--") + $stagedPaths) | Out-Null
        } else {
            Invoke-Git @("reset", "HEAD") | Out-Null
        }
    } else {
        Write-Log "Committed: $commitMsg"
        $pushOut = Invoke-Git @("push")
        $pushCode = $script:gitCode
        if ($pushOut) { Write-Log "git push: $($pushOut -join ' | ')" }
        if ($pushCode -ne 0) {
            Write-Log "git push failed (exit $pushCode) - commit is local only." "WARN"
        } else {
            Write-Log "Pushed to remote successfully."
        }
    }
} else {
    Write-Log "No public output changes to commit."
}

Write-Log "=== Daily pipeline complete ==="
$briefDate = Get-Date -Format "yyyy-MM-dd"
Write-Log "Daily brief: docs\briefs\$briefDate.md"

exit 0
