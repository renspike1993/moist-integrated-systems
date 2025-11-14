# Activate virtual environment
& "scripts\activate"

# Get the IPv4 address dynamically
$ip = (Get-NetIPAddress -AddressFamily IPv4 `
      | Where-Object {$_.IPAddress -notlike "127.*"} `
      | Select-Object -First 1 -ExpandProperty IPAddress)

Write-Host "Detected IP: $ip"
Write-Host ""

# Prompt for PostgreSQL password (HIDDEN)
$secure = Read-Host "Enter PostgreSQL password" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
$POSTGRES_PASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
[Environment]::SetEnvironmentVariable("POSTGRES_PASSWORD", $POSTGRES_PASSWORD, "Process")

Write-Host "Password stored for this session only."
Write-Host ""

# Run Django server
python manage.py runserver "$ip`:7000"
