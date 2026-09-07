param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $Arguments
)

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command py -ErrorAction SilentlyContinue
}
if (-not $python) {
    Write-Error "Python 3 is required to run install.py"
    exit 2
}

$scriptPath = Join-Path $PSScriptRoot "install.py"
if ($python.Name -eq "py.exe") {
    & $python.Source -3 $scriptPath @Arguments
} else {
    & $python.Source $scriptPath @Arguments
}
exit $LASTEXITCODE
