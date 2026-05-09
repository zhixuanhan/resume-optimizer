import subprocess, time

# Kill all processes using port 5000
result = subprocess.run(['powershell', '-Command', '''
try {
    $p = Get-NetTCPConnection -LocalPort 5000 -ErrorAction Stop
    $p | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    Write-Host "killed port 5000 processes"
} catch {
    Write-Host "port 5000 not in use"
}
try {
    $p2 = Get-NetTCPConnection -LocalPort 5001 -ErrorAction Stop
    $p2 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
    Write-Host "killed port 5001 processes"
} catch {
    Write-Host "port 5001 not in use"
}
'''], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print('stderr:', result.stderr)

# Kill any stray python processes for resume-optimizer
result2 = subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True, text=True)
print(result2.stdout)

print('done, waiting 2s...')
time.sleep(2)