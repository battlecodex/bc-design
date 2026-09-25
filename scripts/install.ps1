# BC Design System - Universal Multi-Runtime Installer for Windows (PowerShell)
# Supports Claude Code, Codex, Antigravity, and Kiro

param (
    [string]$Ai = "all",
    [string]$TargetDir = "."
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "install.py"

if (Get-Command "py" -ErrorAction SilentlyContinue) {
    py -3 $PythonScript --ai $Ai --target-dir $TargetDir
} elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
    python $PythonScript --ai $Ai --target-dir $TargetDir
} elseif (Get-Command "python3" -ErrorAction SilentlyContinue) {
    python3 $PythonScript --ai $Ai --target-dir $TargetDir
} else {
    Write-Host "Error: Python 3.x is required to run the installer." -ForegroundColor Red
    exit 1
}
